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

<table align="left" widthType="abs" columns="[148.0,346.0,263.0,314.0]" style="width: 1071.0px; border-collapse: collapse;">
<colgroup>
<col style="width: 148.0px;" />
<col style="width: 346.0px;" />
<col style="width: 263.0px;" />
<col style="width: 314.0px;" />
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
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 148px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>方案痛点</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 148px;">

* 极端 Non-IID
* 边 ↔ 边通信困难
* GAN 训练易崩溃
* 大规模扩展性
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 148px;">

* 数据稀缺（小数据端）
* 隐私风险（生成器泄露/数据泄露）
* 移动端算力有限
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 148px;">

* Non-IID 下客户端更新偏差大
* user-level privacy
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>核心机制</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

* <b>CAP 协同博弈</b>（Device→Edge, Edge→Cloud）
* <b>Mix-G</b>（共享+个性化生成器）- 云聚合保证全局一致性
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

* <b>云保留 G，端保留 D</b> → 职责分离
* <b>差分隐私 (DP)</b> 聚合保护
* <b>pHash-KT 投票</b>筛高质量样本
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

* <b>GAN 生成中性样本</b>消除偏差
* 将客户端更新中的偏差项约束，理论+实验保证 unbiased 聚合
</td>
</tr>
<tr>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>应用范围</b></p>
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

* MEC/5G/多小区场景
* 数据分布极端异构（医疗、智慧城市等）
* 通信受限环境
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

* 跨设备 (IoT/手机)
* 数据量小、算力弱、隐私敏感的环境
</td>
<td style="border-style: solid solid solid solid; border-width: 1px 1px 1px 1px; border-color: #cccccc #cccccc #cccccc #cccccc; height: 48px;">

* 一般性联邦学习任务
* Non-IID 数据分布明显的场景（图像分类、NLP 等）
</td>
</tr>
</table>
<div style="clear: left;"></div>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>

### 四、各自注重点的进一步解释

#### 什么是跨设备场景？

> <p style="font-family: SimSun; font-size: 16px;">Cross-device FL refers to a distributed machine learning model where numerous users equipped with potentially lightweight devices and unreliable network connections participate in the training phase [<span style="color: rgb(51, 51, 51);background-color: rgb(255, 255, 255);font-size: 11pt;">Advances and open problems in federated learning</span>]<a href="https://ieeexplore.ieee.org/document/9464278">ieeexplore.ieee.org</a></p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">因为参与设备极多，且设备都很小，算力非常有限，为了保证部署简单、扩展性强 → <b>端设备直接与云服务器通信</b></p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>典型场景：</b>手机键盘输入、可穿戴健康设备、智能家居</p>

#### 什么是MEC 场景？

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">因为参与设备数量中等，且有基站这种固定的边缘基础设施，所以才用 → 端设备（手机/车载设备）连接到 <b>边缘服务器 (Edge)</b>，边缘再和 <b>云 (Cloud)</b> 通信</p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><b>典型场景：车联网 (V2X)、智慧城市、工业物联网</b></p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>

### 五、方案痛点的进一步解释

##### CGL-GAN：

<p style="text-align: unset; font-family: SimSun; font-size: 16px;">CGL-GAN 是这三个中， 唯一真正研究，如何让 Federated GAN 本身在 Non-IID 下跑通的</p>

<img alt="" src="https://clouddocs.huawei.com/koopage/v1/app/api/documents/doc/preview/020327a9-c381-4e5e-8e36-aa937f12a64d?document_id=c470416f-5533-4ff0-9bd0-4c834d80fbf1" title="" align="left"/>

##### Fed-GAN:

<p style="text-align: left; font-family: SimSun; font-size: 16px;">Fed-GAN <span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">更偏向于</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">“</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">全局分布拟合</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">”</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">，通过多客户端知识投票</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">/</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">聚合，生成能代表所有客户端分布的合成数据，提升全局模型对非</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">IID</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">数据的泛化能力，</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">IID</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">化是</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">“</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">整体性的</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">”</span></p>

<p style="text-align: left; font-family: Arial; font-size: 12pt;"><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;"><b>But</b></span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">，实验表明：</span>Fed-GAN 在 Non-IID 下虽然也能运行，但性能显著低于 IID（指标：用合成数据训练 CNN，在真实数据集上测试分类准确率）</p>

<img alt="" src="https://clouddocs.huawei.com/koopage/v1/app/api/documents/doc/preview/cb4eba01-9af8-454e-bdee-00d75ab62641?document_id=c470416f-5533-4ff0-9bd0-4c834d80fbf1" title="" align="left"/>

<p style="text-align: left; font-family: SimSun; font-size: 16px;">而除了表IV外，其他实验均和Non-iid没有关系，而是在测试是否解决了数据稀缺（Fed-GAN 生成数据是否逼真（合成数据的评估指标FID），是否“有用”（用于训练CNN））。</p>

<p style="text-align: left; font-family: SimSun; font-size: 16px;"><span style="color: rgb(244, 36, 31);">通过实验结果可以知道，</span><span style="color: rgb(244, 36, 31);"><b>Fed-GAN 的目标不是解决联邦 GAN 在 Non-IID 下的收敛性问题</b></span><span style="color: rgb(244, 36, 31);">（这是 CGL-GAN 的痛点），而是解决 </span><span style="color: rgb(244, 36, 31);"><b>数据稀缺 + 隐私保护</b></span><b>。</b></p>

##### FLGan:

<p style="font-family: SimSun; font-size: 16px;">FlGan <span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">更强调</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">“</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">个性化数据补齐</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">”</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">，每个客户端通过外部生成器补足自己缺失的类别，从而本地数据变得</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;"> IID，</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">真正实现了</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">“</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">本地的</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">IID</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;">化</span><span style="color: rgb(31, 35, 40);background-color: rgb(255, 255, 255);font-size: 12pt;font-family: Arial;">”</span></p>

<img alt="" src="https://clouddocs.huawei.com/koopage/v1/app/api/documents/doc/preview/7c6ffdbc-8784-449b-8da3-d43ac0224041?document_id=c470416f-5533-4ff0-9bd0-4c834d80fbf1" title="" align="left"/>

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

1. 方向上：CGL-GAN是唯一实现了在Non-iid下的联邦GAN训练

2. 架构上：CGL-GAN的架构是联邦GAN领域的进一步改进，而FLGAN只是典型的联邦场景

3. 隐私上：CGL-GAN在隐私保护上有改进可做

4. 复现上：CGL-GAN代码开源，<span style="color: rgb(244, 36, 31);">可以更好的去测试和改进方案</span>在Non-iid下的效果

5. 实验对比上：CGL-GAN的开源代码还包含对比方案ACGAN、FLGAN、MDGAN的代码

<p style="text-align: unset; font-family: SimSun; font-size: 16px;"><br /></p>
