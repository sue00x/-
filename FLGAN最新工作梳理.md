### 一、可以用作对比的文献

* FlGan: GAN-Based Unbiased Federated Learning Under Non-IID Settings | TKDE 2024 | <a href="https://ieeexplore.ieee.org/abstract/document/10234084">ieeexplore.ieee.org</a>

* A Novel Federated Learning Scheme for Generative Adversarial Networks | TMC 2024 | <a href="https://ieeexplore.ieee.org/document/10130621">ieeexplore.ieee.org</a> | <a href="https://github.com/NetworkCommunication/CGL-GAN">github.com</a>

* Fed-GAN: Federated Generative Adversarial Network with Privacy-Preserving for Cross-Device Scenarios | TDSC 2025 | <a href="https://ieeexplore.ieee.org/abstract/document/10989588">ieeexplore.ieee.org</a> | <a href="https://github.com/daxx1/fed-gan">github.com</a>

### 二、它们的痛点

* FlGan：为了解决 Non-IID 偏差 → 生成近似 IID 的补充分布

* CGL-GAN：为了解决 Non-IID 下“联邦 GAN 难以跑通”的问题 → 设计稳定架构和生成器分层

* Fed-GAN：为了解决数据稀缺 + 隐私风险 → 用云端合成补数据

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>

### 三、不同：

<table align="left" widthType="abs" columns="[58.0,346.0,263.0,279.0]" style="width: 946.0px; border-collapse: collapse;">
<colgroup>
<col style="width: 58.0px;" />
<col style="width: 346.0px;" />
<col style="width: 263.0px;" />
<col style="width: 279.0px;" />
</colgroup>
<tr>
<th style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">维度</p>
</th>
<th style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">
<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>CGL-GAN</b></p>
</th>
<th style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">
<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>Fed-GAN</b></p>
</th>
<th style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">
<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>FlGan</b></p>
</th>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>框架结构</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>三层：云–边–端</b>端 = 判别器 D边 = 生成器 G（Mix-G: 共享层+个性化层）云 = 全局聚合/协调</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>三层：云–雾(聚合)–端</b>端 = 判别器 D云 = 生成器 G雾/聚合层 = DP 聚合 + pHash-KT 投票</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>两层：服务器–客户端</b>在标准联邦学习结构中引入 GAN，对全局更新做偏差消除</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>框架设计目的</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">面向 <b>MEC 场景</b>，解决通信限制 + 极端异构性，保证 GAN 稳定收敛</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">面向 <b>跨设备场景</b>，解决资源受限 + 隐私保护 + 数据稀缺问题</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">面向 <b>通用联邦学习</b>，解决 Non-IID 下局部分布偏差，保证全局模型 unbiased</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">框架本质</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">设备 + 边缘服务器 + 云</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">可能有“聚合节点/雾节点”做中转，<span style="color: rgb(244, 36, 31);">但本质是 </span><span style="color: rgb(244, 36, 31);"><b>端–云模式</b></span></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">传统的联邦学习结构：客户端 (Client)+服务器 (Server)</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>方案痛点</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 极端 Non-IID</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 边 ↔ 边通信困难</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- GAN 训练易崩溃- 大规模扩展性</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 数据稀缺（小数据端）</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 隐私风险（生成器泄露/数据泄露）</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 移动端算力有限</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- Non-IID 下客户端更新偏差大</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- FedAvg 等方法收敛慢/准确率低</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>核心机制</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>CAP 协同博弈</b>（Device→Edge, Edge→Cloud）</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>Mix-G</b>（共享+个性化生成器）- 云聚合保证全局一致性</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>云保留 G，端保留 D</b> → 职责分离</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>差分隐私 (DP)</b> 聚合保护</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>pHash-KT 投票</b>筛高质量样本</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>GAN 生成中性样本</b>消除偏差</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 将客户端更新中的偏差项约束，理论+实验保证 unbiased 聚合</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>应用范围</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- MEC/5G/多小区场景</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 数据分布极端异构（医疗、智慧城市等）</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 通信受限环境</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 跨设备 (IoT/手机)</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 数据量小、算力弱、隐私敏感的环境</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 一般性联邦学习任务</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- Non-IID 数据分布明显的场景（图像分类、NLP 等）</p>
</td>
</tr>
</table>
<div style="clear: left;"></div>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>

### 四、各自注重点的进一步解释

#### 什么是跨设备场景？

> <p style="font-family: SimSun; font-size: 16px;">Cross-device FL refers to a distributed machine learning model where numerous users equipped with potentially lightweight devices and unreliable network connections participate in the training phase [<span style="color: rgb(51, 51, 51);background-color: rgb(255, 255, 255);font-size: 11pt;">Advances and open problems in federated learning</span>]</p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">因为参与设备极多，且设备都很小，算力非常有限，为了保证部署简单、扩展性强 → <b>端设备直接与云服务器通信</b></p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>典型场景：</b>手机键盘输入、可穿戴健康设备、智能家居</p>

#### 什么是MEC 场景？

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">因为参与设备数量中等，且有基站这种固定的边缘基础设施，所以才用 → 端设备（手机/车载设备）连接到 <b>边缘服务器 (Edge)</b>，边缘再和 <b>云 (Cloud)</b> 通信</p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>典型场景：车联网 (V2X)、智慧城市、工业物联网</b></p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>

### 五、方案痛点的进一步解释

#### 🔹 两种“解决 Non-IID”思路

1. <b>纠偏式解决 (bias correction)</b>

    * 假设我们希望全局模型能真实反映所有客户端的数据分布。

    * 方法：对齐/融合各端的 <b>真实 Non-IID 分布</b>，减少因数据异构导致的 <b>偏差 (bias)</b>。

    * 代表：<b>FlGan</b>（用 GAN 生成“中性样本”抵消偏差）、<b>CGL-GAN</b>（用共享+个性化生成器保持本地差异同时收敛）。

2. <b>规避式解决 (bypass / ignore)</b>

    * 不去对齐各端真实分布，而是 <b>直接生成一个统一的近似 IID 数据分布</b>，强行补足数据稀缺问题。

    * 方法：让所有客户端共享同一份“公共数据”，这样训练起来看起来像 IID。

    * 代表：<b>Fed-GAN</b>。

#### 🔹 Fed-GAN 为什么“不算真正的 Non-IID 解决方案”？

* <b>Fed-GAN 的目标是数据稀缺</b>：<br> 它关心的是 “设备端数据太少，如何凑够样本” → 于是生成全局 IID 样本来补足。

* <b>它没有处理各端的真实差异</b>：<br> 如果 A 端全是猫，B 端全是狗，C 端全是鸟：

    * <b>FlGan</b> 会尝试消除因为这种差异导致的偏差；

    * <b>CGL-GAN</b> 会保留各自特征，同时保证 GAN 收敛；

    * <b>Fed-GAN</b> 直接生成“猫+狗+鸟”的全局 IID 样本 → 每个端都拿一份，训练时看起来像 IID。

* 所以 <b>Fed-GAN 并不是在修复 Non-IID 带来的偏差，而是在“覆盖/绕过” Non-IID</b>。<br> 换句话说，它不是在“理解 Non-IID 并对齐它”，而是在“忽略 Non-IID 差异，用统一分布代替”。

#### 🔑 总结类比

* <b>FlGan</b>：医生 → 发现数据分布有偏差，给你做 <b>矫正</b>。

* <b>CGL-GAN</b>：调解人 → 保留每个人的个性，但帮你们找到 <b>共同收敛</b> 的方式。

* <b>Fed-GAN</b>：大锅饭 → 不管你原来吃什么，先给大家端一碗 <b>统一的饭 (IID 数据)</b>，这样就能凑合训练了。

<p style="font-family: SimSun; font-size: 16px;">✅ 所以说：</p>

* <b>Fed-GAN 的确能缓解 Non-IID 的影响</b>，但它的方式是 <b>绕开 (bypass)</b> 而不是 <b>真正解决 (correct)</b>。

* 在学术语境下，通常把 Fed-GAN 定位为 <b>解决数据稀缺 &amp; 隐私问题</b>，而 <b>FlGan/CGL-GAN 才是直接针对 Non-IID 设计</b>。

<p style="font-family: SimSun; font-size: 16px;"><br /></p>

### 六、隐私性对比

<table align="left" widthType="abs" columns="[76.0,457.0,414.0]" style="width: 947.0px; border-collapse: collapse;">
<colgroup>
<col style="width: 76.0px;" />
<col style="width: 457.0px;" />
<col style="width: 414.0px;" />
</colgroup>
<tr>
<th style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">维度</p>
</th>
<th style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">
<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>CGL-GAN</b></p>
</th>
<th style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">
<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>Fed-GAN</b></p>
</th>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>框架架构</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">云–边–端端=D，边=G，云=全局协调</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">云–雾(聚合)–端端=D，云=G，雾层做DP聚合</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 120px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>主要敏感环节</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 120px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">① 端→边：上传 D 的梯度/参数</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">② 边→端：下发生成样本（可能过拟合）</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">③ 边→云：上传生成器参数</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">④ 云→边：下发全局 G</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 120px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">① 端→雾：上传 D 的梯度</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">② 雾→云：上传聚合后的梯度</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">③ 云：训练生成器 G</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>潜在隐私风险</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 梯度反演攻击 (从 D 梯度恢复端数据)</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- GAN inversion (生成样本暴露局部分布)</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 边/云模型参数泄露局部特征</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 梯度反演攻击 (设备级)</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 模型反演攻击 (云端 G 恢复用户数据)</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- GAN 输出泄露个体样本</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>DP 使用情况</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">❌ 没有内置 DP（论文重点是通信与收敛，不关注隐私）</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">✅ 在 <b>端→雾、雾→云</b> 环节对梯度加噪声，保证 (ε,δ)-DP</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>隐私保护目标</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 没有专门隐私机制</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- 默认假设 MEC 场景下数据敏感性相对较低（如交通/工业数据）</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>用户级隐私</b>：保护单个设备数据</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>群体级隐私</b>：聚合后仍保护区域统计特征</p>
<p style="text-align: unset; font-family: SimSun; font-size: 16px;">- <b>防模型反演</b>：云端 G 不能恢复原始样本</p>
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>代表性安全性</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">更关注 <b>Non-IID 收敛 &amp; 通信效率</b>，隐私保护不足</p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">更关注 <b>用户隐私保护 &amp; 数据稀缺补足</b>，DP 是必需组件</p>
</td>
</tr>
</table>
<div style="clear: left;"></div>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>

### 七、可做方向

<p style="text-align: start; font-family: SimSun; font-size: 16px;">用CGL-GAN作为对比文章，一方面增加隐私保护，一方面增强它在Non-iid下的FL性能</p>

<p style="text-align: start; font-family: SimSun; font-size: 16px;"><br /></p>

<p style="text-align: start; font-family: SimSun; font-size: 16px;">好处：</p>

1. 方向上：CGL-GAN是真的联邦GAN，且考虑了Non-iid问题

2. 架构上：CGL-GAN的架构是联邦GAN领域的进一步改进，而FLGAN只是典型的联邦场景

3. 隐私上：CGL-GAN在隐私保护上有改进可做

4. 复现上：CGL-GAN代码开源，<span style="color: rgb(244, 36, 31);">可以更好的去测试和改进方案</span>在Non-iid下的效果

5. 实验对比上：CGL-GAN的开源代码还包含对比方案ACGAN、FLGAN、MDGAN的代码

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>
