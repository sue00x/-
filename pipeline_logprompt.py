
# -*- coding: utf-8 -*-
"""
pipeline.py — 清爽、独立的一键流水线
=================================
特性：
- 单文件完成：候选生成 → 轻量修复 → 评测 → 轻量进化（可选）→（可选）结构化解释
- 默认规则抽取；仅当 --mode ai_try 时尝试调用 LLM，且严格“只保留在原日志中出现过的行”
- 不依赖原有的 report_gen/selfcheck/evaluator/evolve 等多脚本

输入：
  --logs  logs.jsonl  （{id, log}）
  --gold  gold_full.jsonl 或 gold_short.jsonl （{id, report}）
输出（位于 --out 目录）：
  candidates.jsonl, repaired.jsonl, metrics.jsonl, new_constraints.txt（可选）, explanations.jsonl（可选）

用法示例：
  python pipeline.py --logs ./preprocess/logs.jsonl --gold ./preprocess/gold_full.jsonl \
    --out ./out/lite --span full --mode ai_try --compact --evolve --explain json
"""
import argparse, os, json, re, statistics, pathlib
from typing import List, Dict

SYZBOT_RULES = """You are extracting a syzbot-style crash report from a Linux kernel log.
STRICT RULES:
- Output ONLY raw lines that appear VERBATIM in the input logs (you may drop leading timestamps like "[ 12.345]").
- Follow the section order if present in the logs: 
  1) BUG/KASAN lines
  2) "Read/Write of size ..." line
  3) "CPU:" line (and optional "Hardware name:")
  4) "Call Trace:" and subsequent stack frames (skip tool frames like dump_stack/kasan_report/__asan_/printk)
  5) KASAN details: "Allocated by task", "Freed by task", "The buggy address...", "Memory state around..."
- Do NOT invent or rewrite text. If a section is missing, omit it (no commentary).
- No JSON, no explanations, no tags, no headings, no extra punctuation."""

def build_syzbot_messages(log_text: str, fewshots=None):
    """few-shot 模仿 syzbot 报告的行级拷贝输出（比原 build_llm_messages 约束更强）。"""
    msgs=[{"role":"system","content":SYZBOT_RULES}]
    fs = fewshots or DEFAULT_FEWSHOT
    # few-shot：用户日志 -> 助手原文拷贝式“报告”
    for ex in fs:
        msgs.append({"role":"user","content":f"# Logs\n{ex['log']}".strip()})
        msgs.append({"role":"assistant","content":ex["report"].strip()})
    # 目标样本
    msgs.append({"role":"user","content":f"# Logs\n{log_text}".strip()})
    return msgs


# ---------- 可选：LLM（仅 ai_try/explain 时使用） ----------
try:
    from llm_client import LLMClient
except Exception:
    LLMClient = None

# ---------- 规范化 & 正则 ----------
TS  = re.compile(r'^(?:\s*\[[^\]]+\]\s*)+', re.I)
def _norm(s: str) -> str:
    return TS.sub('', (s or '').rstrip())

BUG = re.compile(r'BUG:\s*KASAN:', re.I)
RW  = re.compile(r'\b(?:Read|Write)\s+of\s+size\s+\d+', re.I)
CT  = re.compile(r'\bCall Trace:\s*$', re.I)
CPU = re.compile(r'^CPU:\s+.*Not tainted', re.I)
RIP = re.compile(r'^\s*RIP:\s', re.I)
RSP = re.compile(r'^\s*RSP:\s', re.I)
CODE     = re.compile(r'^\s*Code:\s', re.I)
ALLOCATED_BY = re.compile(r'^\s*Allocated by task', re.I)
FREED_BY     = re.compile(r'^\s*Freed by task', re.I)
BUGGY_ADDR   = re.compile(r'^\s*The buggy address (belongs|is located)', re.I)
MEM_AROUND   = re.compile(r'^\s*Memory state around', re.I)
PANIC    = re.compile(r'^\s*Kernel panic\b', re.I)
MODULES  = re.compile(r'^\s*Modules linked in:', re.I)
HARDWARE = re.compile(r'^\s*Hardware name:', re.I)

SKIP_PREFIX = re.compile(
    r'^(?:dump_stack|show_stack|print_address|print_report|kasan_report|__pfx_|__warn|'
    r'warn_slowpath|__virt_addr_valid|kasan_|__asan_|_printk|printk|vprintk|report_bug)\b',
    re.I
)

# 可选：tiktoken，用于 token 预算（没有也能运行，会退化为“字符//3”估算）
try:
    import tiktoken
    _HAS_TIKTOKEN = True
except Exception:
    _HAS_TIKTOKEN = False

def _token_len(s: str, model: str) -> int:
    # 对非 OpenAI 模型（如 Qwen），直接用字符/3 估算 token
    return max(1, len(s) // 3)


def _split_single_long_log(log_text: str, max_lines=200, stride=180):
    """对单条（可能很长的）日志做按行切块，带重叠窗口，避免割裂关键锚点。"""
    lines = [x for x in (log_text or "").splitlines() if x.strip()]
    if len(lines) <= max_lines:
        return [log_text]
    out, i = [], 0
    while i < len(lines):
        out.append("\n".join(lines[i:i+max_lines]))
        if i + max_lines >= len(lines):
            break
        i += stride
    return out

def _build_fx_fz_header(no_reason=True):
    """
    fz：受控输出模板，强制逐编号回应，只允许复制原文子串；可选是否带 reason。
    """
    fmt = (
        "Organize your answer in the following format:\n"
        "(1) {x}\n(2) {x}\n...\n"
        "Rules:\n"
        "- ONLY copy substrings that appear VERBATIM in the input logs.\n"
        "- Keep the original order; be concise; no extra commentary.\n"
    )
    if no_reason:
        fmt = fmt.replace("{x}", "x")
    else:
        fmt = fmt.replace("{x}", "x-y").replace(
            "no extra commentary.", "append a concise reason y after x; no extra commentary besides x-y."
        )
    return fmt + "\nThere are !!NumberControl!! logs, the logs begin:\n!!FormatControl!!\n"

def _make_logprompt_batches(chunks, model, token_budget=2800, no_reason=True):
    """
    把若干 chunk 编号成 (i) ...，按 token 预算打包成多条 prompt。
    返回：prompts: List[str], id_groups: List[List[int]]  （每条 prompt 对应的全局编号列表）
    """
    header_tpl = _build_fx_fz_header(no_reason=no_reason)
    prompts, id_groups = [], []
    fmt_lines, cur_msgs, cur_ids = [], [], []

    def _header_for(n:int):
        return header_tpl.replace("!!NumberControl!!", str(n)).replace("!!FormatControl!!", "".join(fmt_lines))

    def _flush():
        nonlocal fmt_lines, cur_msgs, cur_ids
        if cur_msgs:
            prompts.append(_header_for(len(cur_msgs)) + " " + " ".join(cur_msgs))
            id_groups.append(cur_ids[:])
        fmt_lines, cur_msgs, cur_ids = [], [], []

    base_tokens = _token_len(_header_for(1), model)  # 近似，给头部预留空间
    cur_tokens = base_tokens
    for gid, content in chunks:
        piece = f"({gid}) {content}"
        need = _token_len(piece, model)
        if not cur_msgs:
            cur_msgs.append(piece); cur_ids.append(gid)
            fmt_lines.append(f"({gid}) x\n" if no_reason else f"({gid}) x-y\n")
            cur_tokens = base_tokens + need
            continue
        if cur_tokens + need <= token_budget:
            cur_msgs.append(piece); cur_ids.append(gid)
            fmt_lines.append(f"({gid}) x\n" if no_reason else f"({gid}) x-y\n")
            cur_tokens += need
        else:
            _flush()
            cur_msgs.append(piece); cur_ids.append(gid)
            fmt_lines.append(f"({gid}) x\n" if no_reason else f"({gid}) x-y\n")
            cur_tokens = base_tokens + need
    _flush()
    return prompts, id_groups

def _align_fx_fz_answer_to_chunks(answer_text: str, gids: list):
    """
    把模型对某条 prompt 的回答，按 (gid)->(gid_next) 切成与各 chunk 一一对应的片段。
    返回：{gid: segment_text}
    """
    s = (answer_text or "").replace("\n", " ")
    out = {}
    for a, b in zip(gids, gids[1:]):
        m = re.search(rf"\({a}\)\s*(.*?)\s*\({b}\)", s)
        if m: out[a] = m.group(1).strip()
    if gids:
        last = gids[-1]
        m2 = re.search(rf"\({last}\)\s*(.*)$", s)
        if m2: out[last] = m2.group(1).strip()
    return out

# ---------- 基础 IO ----------
def read_jsonl(path: str):
    rows = []
    with open(path,'r',encoding='utf-8') as f:
        for ln in f:
            ln=ln.strip()
            if not ln: continue
            try: rows.append(json.loads(ln))
            except: pass
    return rows

def write_jsonl(rows, path: str):
    with open(path,'w',encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False)+'\n')

def load_map(path: str, key='id', val='report'):
    mp={}
    for o in read_jsonl(path):
        mp[o[key]] = o.get(val,'')
    return mp

# ---------- 规则抽取 ----------
def extract_slice_from_log(raw: str, max_lines: int = 5):
    if not isinstance(raw, str) or not raw.strip():
        return []
    lines=[_norm(x) for x in raw.splitlines() if x.strip()]

    bug = next((x for x in lines if BUG.search(x)), None)
    rw  = next((x for x in lines if RW.search(x)), None)
    ct_idx = next((i for i,x in enumerate(lines) if CT.search(x)), None)
    ct = lines[ct_idx] if ct_idx is not None else None

    frame=None
    if ct_idx is not None:
        for j in range(ct_idx+1, min(ct_idx+20, len(lines))):
            cand = lines[j].strip()
            if cand and not SKIP_PREFIX.search(cand):
                frame = cand; break
    cpu = next((x for x in lines if CPU.search(x)), None)

    out=[]
    if bug: out.append(bug)
    if rw:  out.append(rw)
    if ct:  out.append(ct)
    if frame: out.append(frame)
    if cpu: out.append(cpu)
    return out[:max_lines]

def _collect_block(lines, start_idx, stop_pred, max_next=64):
    out=[lines[start_idx]]
    for j in range(start_idx+1, min(len(lines), start_idx+1+max_next)):
        s=lines[j]
        if not s.strip(): break
        if stop_pred(s): break
        out.append(s)
    return out

def _collect_until_blank_or(pivot_idx, lines, extra_pred=None, max_next=16):
    out=[]
    for j in range(pivot_idx+1, min(len(lines), pivot_idx+1+max_next)):
        s=lines[j]
        if not s.strip(): break
        if extra_pred and extra_pred(s): break
        out.append(s)
    return out

def extract_full_from_log(raw: str, max_frames: int = 64):
    if not isinstance(raw, str) or not raw.strip():
        return []
    lines=[_norm(x) for x in raw.splitlines()]

    out=[]
    # 环境
    for pat in (PANIC, MODULES, HARDWARE):
        m = next((ln for ln in lines if ln and pat.search(ln)), None)
        if m and m not in out: out.append(m)
    # BUG/RW
    for pat in (BUG, RW):
        m = next((ln for ln in lines if ln and pat.search(ln)), None)
        if m and m not in out: out.append(m)
    # RIP/RSP + REGs
    rip_idx = next((i for i,s in enumerate(lines) if s and RIP.search(s)), None)
    if rip_idx is not None:
        out.append(lines[rip_idx])
        regs = _collect_until_blank_or(rip_idx, lines, extra_pred=lambda s: CT.search(s) or CPU.search(s) or CODE.search(s), max_next=20)
        regs = [r for r in regs if re.search(r'^(R..:|[A-Z]{2,4}:)', r)]
        out.extend(regs)
    rsp_idx = next((i for i,s in enumerate(lines) if s and RSP.search(s)), None)
    if rsp_idx is not None and lines[rsp_idx] not in out:
        out.append(lines[rsp_idx])
    # Code
    code_idx = next((i for i,s in enumerate(lines) if s and CODE.search(s)), None)
    if code_idx is not None:
        out.append(lines[code_idx])
        out.extend(_collect_until_blank_or(code_idx, lines, extra_pred=lambda s: CT.search(s) or CPU.search(s), max_next=16))
    # CPU
    cpu_line = next((ln for ln in lines if ln and CPU.search(ln)), None)
    if cpu_line and cpu_line not in out: out.append(cpu_line)
    # Call Trace + frames
    ct_idx = next((i for i,s in enumerate(lines) if s and CT.search(s)), None)
    if ct_idx is not None:
        out.append(lines[ct_idx])
        frames=[]
        for j in range(ct_idx+1, min(ct_idx+1+max_frames*2, len(lines))):
            cand = lines[j].strip()
            if not cand: break
            if SKIP_PREFIX.search(cand): continue
            frames.append(lines[j])
            if len(frames)>=max_frames: break
        out.extend(frames)
    # KASAN details
    for pat in (ALLOCATED_BY, FREED_BY, BUGGY_ADDR, MEM_AROUND):
        idx = next((i for i,s in enumerate(lines) if s and pat.search(s)), None)
        if idx is not None:
            blk = _collect_block(lines, idx, lambda s: BUG.search(s) or CT.search(s) or CPU.search(s), max_next=32)
            out.extend(blk)

    # 去重
    out2, seen = [], set()
    for s in out:
        if not s or not s.strip(): continue
        if s in seen: continue
        out2.append(s); seen.add(s)
    if not out2: out2 = extract_slice_from_log(raw)
    return out2

# ---------- LLM 尝试与净化 ----------
HARD_RULES = """You are a formatter that extracts a syzbot-style report from a Linux kernel log.
STRICT RULES:
- Output ONLY raw lines that appear VERBATIM in the log (you may drop leading timestamps like "[ 12.345 ]").
- No explanations. No JSON. No tags. No <think>. Output the lines only.
"""

DEFAULT_FEWSHOT = [
    {"log":
     "[  11.11] BUG: KASAN: use-after-free in foo+0x1/0x10\n"
     "[  11.12] Read of size 8 at addr ffff... by task T/123\n"
     "[  11.13] Call Trace:\n"
     "[  11.14] dump_stack_lvl+0x1/0x100\n"
     "[  11.15] bar+0x20/0x60\n"
     "[  11.16] CPU: 0 PID: 123 Not tainted 6.1.0 #1\n",
     "report":
     "BUG: KASAN: use-after-free in foo+0x1/0x10\n"
     "Read of size 8 at addr ffff... by task T/123\n"
     "Call Trace:\n"
     "bar+0x20/0x60\n"
     "CPU: 0 PID: 123 Not tainted 6.1.0 #1"
    }
]

def compress_log_for_llm(raw: str, span: str = "full",
                         win_before: int = 5, win_after: int = 20, max_total_lines: int = 1200):
    src = (raw or "").splitlines()
    lines = [_norm(x) for x in src]
    idxs = []
    pats = [BUG, RW, CT, CPU, RIP, RSP, CODE, ALLOCATED_BY, FREED_BY, BUGGY_ADDR, MEM_AROUND, PANIC, MODULES, HARDWARE]
    for i, s in enumerate(lines):
        if not s.strip(): continue
        for p in pats:
            if p.search(s): idxs.append(i); break
    if not idxs:
        keep = [s for s in lines if s.strip()]
        if len(keep) > max_total_lines:
            step = max(1, len(keep)//max_total_lines)
            keep = keep[::step]
        return "\n".join(keep)
    marked=set()
    for i in idxs:
        left=max(0, i-win_before); right=min(len(lines), i+win_after+1)
        for j in range(left, right):
            if lines[j].strip(): marked.add(j)
    keep=[lines[j] for j in sorted(marked)]
    if len(keep) > max_total_lines:
        step=max(1, len(keep)//max_total_lines); keep=keep[::step]
    return "\n".join(keep)

def build_llm_messages(log_text: str, fewshots=None):
    msgs=[{"role":"system","content":HARD_RULES}]
    fs = fewshots or DEFAULT_FEWSHOT
    for ex in fs:
        msgs.append({"role":"user","content":f"# Logs\n{ex['log']}".strip()})
        msgs.append({"role":"assistant","content":ex["report"].strip()})
    msgs.append({"role":"user","content":f"# Logs\n{log_text}".strip()})
    return msgs

def sanitize_from_log(raw_out: str, log_text: str, span: str = "slice",
                      max_lines_slice: int = 5, max_lines_full: int = 300):
    if not isinstance(raw_out, str): return []
    out = re.sub(r'<think>.*?</think>', '', raw_out, flags=re.S | re.I)
    out = re.sub(r'```.*?```', '', out, flags=re.S)
    out = out.strip()
    log_lines = [_norm(x) for x in (log_text or '').splitlines() if x.strip()]
    keep=[]
    for ln in out.splitlines():
        ln2=_norm(ln)
        if ln2 and any(ln2 in L for L in log_lines):
            keep.append(ln2)
    if not keep: return []
    joined = "\n".join(keep)
    if not (BUG.search(joined) or RW.search(joined) or CT.search(joined)):
        return []
    keep = keep[: (max_lines_slice if span=="slice" else max_lines_full) ]
    return keep

# ---------- 轻量“修复” ----------
def lite_repair(txt: str, span: str = "slice", mode: str = "full"):
    lines=[_norm(x) for x in (txt or '').splitlines() if x.strip()]
    if not lines:
        return ""

    # none 模式
    if mode == "none":
        return "\n".join(lines)

    # slice 模式
    if mode == "slice" or (mode in ["full","balanced","conservative"] and span == "slice"):
        want=[]
        bug = next((x for x in lines if BUG.search(x)), None)
        rw  = next((x for x in lines if RW.search(x)), None)
        ct_idx = next((i for i,x in enumerate(lines) if CT.search(x)), None)
        ct = lines[ct_idx] if ct_idx is not None else None
        frame=None
        if ct_idx is not None:
            for j in range(ct_idx+1, min(ct_idx+15, len(lines))):
                s=lines[j].strip()
                if s and not SKIP_PREFIX.search(s): frame=s; break
        cpu = next((x for x in lines if CPU.search(x)), None)
        for x in (bug,rw,ct,frame,cpu):
            if x and x not in want: want.append(x)
        return "\n".join(want[:5])

    # full 系列模式
    order=[PANIC, MODULES, HARDWARE, BUG, RW, RIP, RSP, CODE, CPU, CT, ALLOCATED_BY, FREED_BY, BUGGY_ADDR, MEM_AROUND]
    want=[]; used=set()
    for pat in order:
        for s in lines:
            if s in used: continue
            if pat.search(s):
                want.append(s); used.add(s)

    # frames
    if any(CT.search(x) for x in want):
        frames=[]
        try:
            start = next(i for i,s in enumerate(lines) if CT.search(s))
            for j in range(start+1, len(lines)):
                ss = lines[j].strip()
                if not ss: break

                # 工具帧过滤
                if mode == "full":
                    if SKIP_PREFIX.search(ss): continue
                elif mode == "balanced":
                    if re.search(r'^(dump_stack|kasan_report|__asan_|printk)\b', ss, re.I):
                        continue
                elif mode == "conservative":
                    pass  # 不过滤

                frames.append(lines[j])

                # 帧上限
                if mode == "full" and len(frames) >= 64:
                    break
                if mode == "balanced" and len(frames) >= 256:
                    break
                # conservative 不限帧
        except StopIteration:
            pass
        want.extend(frames)

    return "\n".join(want)


# ---------- 评测 ----------
def tokenize_lines(txt): return [_norm(x) for x in (txt or "").splitlines() if x.strip()]

def jaccard(a_lines, b_lines):
    sa, sb = set(a_lines), set(b_lines)
    if not sa and not sb: return 1.0
    return len(sa & sb) / max(1, len(sa | sb))

def field_hits(lines):
    def hit(pat): return 1 if any(pat.search(x) for x in lines) else 0
    return {"bug":hit(BUG),"rw":hit(RW),"ct":hit(CT),"cpu":hit(CPU)}

def coverage_bits(lines):
    def hit(p): return 1 if any(p.search(x) for x in lines) else 0
    rip = hit(RIP); rsp = hit(RSP)
    code = hit(CODE); alloc=hit(ALLOCATED_BY); freed=hit(FREED_BY); buggy=hit(BUGGY_ADDR); mem=hit(MEM_AROUND)
    cov_cnt = (1 if (rip or rsp) else 0) + code + alloc + freed + buggy + mem
    total_targets = 1 + 5
    return {"has_rip_or_rsp":1 if (rip or rsp) else 0, "has_code":code,"has_alloc":alloc,
            "has_freed":freed,"has_buggy_addr":buggy,"has_mem_around":mem,
            "coverage_rate": cov_cnt/total_targets}

def count_frames(lines):
    frames, tool, dup = 0, 0, 0; seen=set()
    try: start = next(i for i,x in enumerate(lines) if CT.search(x))
    except StopIteration: return {"stack_depth":0, "noise_rate":0.0}
    for j in range(start+1, len(lines)):
        s = lines[j].strip()
        if not s: break
        if s in seen: dup += 1; continue
        seen.add(s)
        if SKIP_PREFIX.search(s): tool += 1; continue
        frames += 1
    total = frames + tool + dup
    noise = (tool + dup)/total if total>0 else 0.0
    return {"stack_depth":frames, "noise_rate":noise}

def compute_all_metrics(pred_lines, gold_lines):
    """给定预测行与gold行，计算一套指标；若任一为空则返回全None。"""
    if not gold_lines:
        return {"jaccard": None, "field_hit_rate": None, "coverage_rate": None,
                "stack_depth": None, "noise_rate": None, "order_ok": None}
    if not pred_lines:
        return {"jaccard": None, "field_hit_rate": None, "coverage_rate": None,
                "stack_depth": None, "noise_rate": None, "order_ok": None}
    d = {}
    d["jaccard"] = jaccard(pred_lines, gold_lines)
    f = field_hits(pred_lines)
    d["field_hit_rate"] = (sum(f.values()) / 4.0)
    d.update(coverage_bits(pred_lines))
    d.update(count_frames(pred_lines))
    d["order_ok"] = order_ok(pred_lines)
    return d


def order_ok(lines):
    def idx(p):
        for i,x in enumerate(lines):
            if p.search(x): return i
        return 10**9
    seq=[min(idx(PANIC), idx(MODULES), idx(HARDWARE)),
         min(idx(BUG), idx(RW)),
         min(idx(RIP), idx(RSP)),
         idx(CODE),
         idx(CPU),
         idx(CT),
         min(idx(ALLOCATED_BY), idx(FREED_BY), idx(BUGGY_ADDR)),
         idx(MEM_AROUND)]
    seq2=[x for x in seq if x<10**9]
    return int(all(seq2[i] <= seq2[i+1] for i in range(len(seq2)-1)))

# ---------- 进化（轻量约束 + few-shot 追加） ----------
THRESH = {"field_hit_rate":0.85, "coverage_rate":0.5, "stack_depth":8, "noise_rate":0.2, "order_ok":0.9, "jaccard":0.3}
LIB = {
    "stack_depth_low": "- 保留至少 8 个非工具帧，跳过 dump_stack/kasan_report/__asan_/printk 等。",
    "noise_high": "- 去除重复帧与工具帧。",
    "coverage_low_regs": "- 若存在 RIP/RSP 与寄存器行，则必须保留（寄存器不超过20行）。",
    "coverage_low_code": "- 若存在 Code: 段，保留该行及其字节转储（≤16行）。",
    "coverage_low_alloc": "- 若存在 'Allocated by task' 段，按原顺序完整收集至空行/下一段。",
    "coverage_low_freed": "- 若存在 'Freed by task' 段，按原顺序完整收集至空行/下一段。",
    "coverage_low_mem": "- 若存在 'Memory state around' 段，完整保留至空行/下一段。",
    "order_bad": "- 段落顺序按：环境→BUG/RW→RIP/RSP→Code→CPU→Call Trace→KASAN细节→Memory。"
}

def evolve_constraints(metrics_rows):
    def pick(name):
        vals=[r.get(name) for r in metrics_rows if r.get(name) is not None]
        return (statistics.mean(vals) if vals else None)
    add=[]
    if (v:=pick("field_hit_rate")) is not None and v<THRESH["field_hit_rate"]:
        add.append(LIB["stack_depth_low"])
    if (v:=pick("coverage_rate")) is not None and v<THRESH["coverage_rate"]:
        add += [LIB["coverage_low_regs"],LIB["coverage_low_code"],LIB["coverage_low_alloc"],LIB["coverage_low_freed"],LIB["coverage_low_mem"]]
    if (v:=pick("stack_depth")) is not None and v<THRESH["stack_depth"]:
        add.append(LIB["stack_depth_low"])
    if (v:=pick("noise_rate")) is not None and v>THRESH["noise_rate"]:
        add.append(LIB["noise_high"])
    if (v:=pick("order_ok")) is not None and v<THRESH["order_ok"]:
        add.append(LIB["order_bad"])
    out=[]; seen=set()
    for c in add:
        if c not in seen: out.append(c); seen.add(c)
    return out

def auto_pick_worst_fewshots(metrics_rows, logs_map, gold_map, K=4):
    xs=[(r.get("jaccard"), r["id"]) for r in metrics_rows if r.get("jaccard") is not None and r["id"] in logs_map and r["id"] in gold_map]
    xs.sort(key=lambda t: t[0])
    out=[]
    for j, gid in xs[:K]:
        out.append({"log": logs_map[gid], "report": gold_map[gid]})
    return out

# ---------- 主流程 ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logs", required=True)
    ap.add_argument("--gold", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--span", choices=["slice","full"], default="slice")
    ap.add_argument("--repair_mode", choices=["none","slice","full","conservative","balanced"], default="full",
                help="选择修复模式: none=不修复, slice=5锚点, full=原规则, conservative=保守(不删帧), balanced=放宽规则")
    ap.add_argument("--mode", choices=["rule","ai_try"], default="rule")
    ap.add_argument("--explain", choices=["off","json"], default="off")
    ap.add_argument("--compact", action="store_true")
    ap.add_argument("--evolve", action="store_true")
    ap.add_argument("--fewshot", default="prompts/fewshot_pool.jsonl")
    ap.add_argument("--merge_reports", action="store_true",
                help="把所有日志的候选/修复报告合并成单文件，便于查看与归档")
    ap.add_argument("--config", default="config.json")
    args = ap.parse_args()

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)
    P=lambda name: str(pathlib.Path(args.out)/name)

    logs = load_map(args.logs, 'id', 'log')
    gold = load_map(args.gold, 'id', 'report')

    fewshots=None
    if os.path.exists(args.fewshot):
        fewshots=[json.loads(ln) for ln in open(args.fewshot,'r',encoding='utf-8') if ln.strip()]

    cfg = json.load(open(args.config,'r')) if os.path.exists(args.config) else {}
    llm=None
    if args.mode=="ai_try" or args.explain=="json":
        if LLMClient is None:
            print("[WARN] LLMClient not available; fallback to rules.")
        else:
            llm = LLMClient(cfg.get("API_URL"), cfg.get("API_KEY"), cfg.get("MODEL"),
                            timeout=int(cfg.get("LLM_TIMEOUT",300)),
                            retries=int(cfg.get("LLM_RETRIES",4)),
                            backoff=float(cfg.get("LLM_BACKOFF",1.6)))

    # 1) candidates
    cand_rows=[]
    for bid, logtxt in logs.items():
        report_lines=[]
        if args.mode=="ai_try" and llm:
            # 0) 从 config 读取/设定分批参数（给默认值，不要求你必须改 config）
            tok_budget = int(cfg.get("token_budget", 2800))
            max_lines  = int(cfg.get("max_lines_per_chunk", 200))
            stride     = int(cfg.get("chunk_stride", 180))
            no_reason  = bool(cfg.get("no_reason", True))  # True=只要 x，False=要 x-y

            # 1) 预压缩（可选）+ 单条日志重叠切块
            ctx = compress_log_for_llm(logtxt, span=args.span) if args.compact else logtxt
            sub_chunks = _split_single_long_log(ctx, max_lines=max_lines, stride=stride)

            # 2) 统一为全局编号 (1..K)，并按 token 预算打包成多条 prompt（fx/fz）
            expanded = [(i+1, ch) for i, ch in enumerate(sub_chunks)]
            prompts, id_groups = _make_logprompt_batches(
                expanded,
                model=cfg.get("MODEL","gpt-3.5-turbo"),
                token_budget=tok_budget,
                no_reason=no_reason
            )

            # 3) 逐批请求 LLM（短消息，显著降低 504），收集每个 chunk 的段落
            chunk_segments = {gid: [] for gid, _ in expanded}
            for p, gids in zip(prompts, id_groups):
                try:
                    out_text = llm.chat(
                        [
                            {"role":"system", "content": SYZBOT_RULES},
                            {"role":"user",   "content": p}
                        ],
                        temperature=float(cfg.get("temperature_report",0.0))
                    )

                except Exception:
                    # 单批失败不影响全局，跳过该批
                    continue
                parts = _align_fx_fz_answer_to_chunks(out_text, gids)
                # 4) 对每个 chunk 的模型输出做“只保留出现在原始 log 中的行”（sanitize）
                for gid, seg in parts.items():
                    # 使用原始 logtxt 做对照，确保绝不引入幻觉
                    kept = sanitize_from_log(seg, logtxt, span=args.span)
                    if kept:
                        chunk_segments[gid].extend(kept)

            # 5) 合并所有 chunk 的行：去重保序
            merged, seen = [], set()
            for gid, _ in expanded:
                for ln in chunk_segments.get(gid, []):
                    if ln not in seen:
                        seen.add(ln)
                        merged.append(ln)

            if merged:
                report_lines = merged

            # 6) 可选：合并所有日志的候选/修复为一个总报告
            if args.merge_reports:
                lines_out = []
                for r in (rep_rows if args.merge_use_repaired else cand_rows):
                    rid = r["id"]
                    body = r["repaired"] if args.merge_use_repaired else r["candidate"]
                    if not body.strip(): 
                        continue
                    lines_out.append("="*66)
                    lines_out.append(f"ID: {rid}")
                    lines_out.append("="*66)
                    lines_out.append(body.rstrip())
                    lines_out.append("")  # 空行分隔
                out_path = P(args.merge_filename)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines_out))
                print(f"[pipeline] Merged report written to {out_path}")


        if not report_lines:
            report_lines = extract_full_from_log(logtxt) if args.span=="full" else extract_slice_from_log(logtxt)
        cand_rows.append({"id":bid, "candidate":"\n".join(report_lines)})
    write_jsonl(cand_rows, P("candidates.jsonl"))

    # 2) repaired（确定性，可选输出）
    if args.repair_mode != "none":
        rep_rows = [{"id": r["id"], "repaired": lite_repair(r["candidate"], span=args.span, mode=args.repair_mode)}
                    for r in cand_rows]
        write_jsonl(rep_rows, P("repaired.jsonl"))
    else:
        rep_rows = [{"id": r["id"], "repaired": ""} for r in cand_rows]  # 保持后续 metrics 计算不出错



    # 3) explanations（可选）
    if args.explain=="json" and llm:
        exp_rows=[]
        tmpl = """From KERNEL LOGS, fill JSON. Use strings; if unknown, "unknown".
{"bug_class":"...","suspect_function":"...","read_write":"read|write|unknown","oob_uaf":"uaf|oob|unknown","top_stack":"...","kernel_version":"...","summary":"...","reason":"..."}
Rules: derive ONLY from text present in logs; JSON only."""
        for bid, logtxt in logs.items():
            ctx = compress_log_for_llm(logtxt, span=args.span) if args.compact else logtxt
            msgs=[{"role":"system","content":tmpl},{"role":"user","content":f"# Logs\n{ctx}"}]
            try:
                out = llm.chat(msgs, temperature=float(cfg.get("temperature_explain",0.2))).strip()
                try: val=json.loads(out)
                except: val={"parse_error":True,"raw":out}
            except Exception as e:
                val={"error":str(e)}
            exp_rows.append({"id":bid,"explain_json":val})
        write_jsonl(exp_rows, P("explanations.jsonl"))

    # 4) metrics
    def _delta(a, b):
        return None if (a is None or b is None) else (b - a)

    metrics = []
    for r in cand_rows:
        gid = r["id"]
        cand = tokenize_lines(r["candidate"])
        repl = tokenize_lines(next((x["repaired"] for x in rep_rows if x["id"] == gid), ""))
        gold_lines = tokenize_lines(gold.get(gid, ""))
        row = {"id": gid}

        # 各自计算
        cand_m = compute_all_metrics(cand, gold_lines)
        repl_m = compute_all_metrics(repl, gold_lines)

        # 带前缀写入
        for k, v in cand_m.items():
            row[f"cand_{k}"] = v
        for k, v in repl_m.items():
            row[f"repaired_{k}"] = v

        # 差值(修复-候选)
        row["Δ_jaccard"]        = _delta(row["cand_jaccard"],        row["repaired_jaccard"])
        row["Δ_field_hit_rate"] = _delta(row["cand_field_hit_rate"], row["repaired_field_hit_rate"])
        row["Δ_coverage_rate"]  = _delta(row["cand_coverage_rate"],  row["repaired_coverage_rate"])
        row["Δ_stack_depth"]    = _delta(row["cand_stack_depth"],    row["repaired_stack_depth"])
        row["Δ_noise_rate"]     = _delta(row["cand_noise_rate"],     row["repaired_noise_rate"])
        row["Δ_order_ok"]       = _delta(row["cand_order_ok"],       row["repaired_order_ok"])

        metrics.append(row)

    write_jsonl(metrics, P("metrics.jsonl"))


    # 5) evolve（轻量）
    if args.evolve:
        constraints = evolve_constraints(metrics)
        with open(P("new_constraints.txt"), 'w', encoding='utf-8') as f:
            for c in constraints: f.write(c+"\n")
        worst = auto_pick_worst_fewshots(metrics, logs, gold, K=int(cfg.get("fewshot_K",4)))
        if worst:
            fs_path = args.fewshot if os.path.exists(os.path.dirname(args.fewshot) or ".") else P("fewshot_pool.jsonl")
            with open(fs_path, 'a', encoding='utf-8') as f:
                for ex in worst: f.write(json.dumps(ex, ensure_ascii=False)+'\n')

    print("[pipeline] Done. Artifacts in", args.out)

if __name__ == "__main__":
    main()
