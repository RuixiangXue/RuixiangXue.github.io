# 生成式世界模型学习笔记

创建时间：2026-07-03

范围：Sora、Cosmos、GAIA、DriveDreamer、Vista、WorldDreamer、Genie。

这份笔记是技术学习材料，不是简历表述。目标是弄清楚每个工作到底在做什么、方法路线有什么差异，以及整个领域如何从视频生成走向可控仿真和具身智能训练。

## 0. 这里说的 world model 是什么

在这组工作里，world model 不能简单理解成“视频生成器”。更有用的定义是：模型能够近似世界在某些条件或动作下如何演化。

可以从五个维度看：

1. **预测**：给定过去观测，预测合理的未来观测。
2. **控制**：未来结果能被动作、轨迹、文本、场景布局、相机姿态等条件控制。
3. **一致性**：保持几何、物体身份、时间、因果关系和物理合理性。
4. **交互性**：人或智能体可以一步一步在生成环境里行动。
5. **有用性**：生成的数据或仿真能真正帮助下游智能体、感知、规划或评测。

这些工作大致可以分成三类：

| 类别 | 代表工作 | 核心思想 |
| --- | --- | --- |
| 通用视频 / 世界模拟器 | Sora, WorldDreamer | 从大规模图像和视频中学习广义视觉动态，world modeling 能力通过规模和时间预测涌现。 |
| 自动驾驶 / Physical AI 世界模型 | GAIA, DriveDreamer, Vista, Cosmos | 在动作、轨迹、场景或传感器条件下生成或预测驾驶 / 物理场景。 |
| 可交互环境生成器 | Genie | 生成可玩的环境，通常从无动作标签视频中学习 latent action。 |

## 1. Sora

资料：

- OpenAI, “Video generation models as world simulators”: https://openai.com/index/video-generation-models-as-world-simulators/
- OpenAI, “Sora: Creating video from text”: https://openai.com/index/sora/

### 1.1 问题

Sora 提出的核心问题是：大规模视频生成模型能不能成为物理世界的模拟器？

它表面上是 text-to-video，但 OpenAI 明确把它放在“学习模拟运动中的物理世界”这个方向上。

### 1.2 输入输出

输入：

- 文本 prompt。
- 静态图像 prompt。
- 已有视频，用于扩展或补全。

输出：

- 高保真视频，支持不同长度、分辨率和宽高比。

### 1.3 模型思想

Sora 的关键抽象是：把图像和视频都表示成 latent space 中的时空 patch 序列。

粗略流程：

1. 把图像 / 视频压缩到 latent code。
2. 把 latent code 切成 spacetime patches。
3. 在这些 patch 上训练 transformer-based diffusion model。
4. 使用不同宽高比、分辨率、时长的图像和视频联合训练。

这和语言模型有一点像：一旦视觉数据被转成 token-like patch sequence，规模、多样性和长上下文就变得非常关键。

### 1.4 为什么重要

Sora 的意义不只是生成效果好，而是它把视频生成重新解释成通向 world simulation 的一条路线。

它不是驾驶专用模型，也没有暴露规划接口，但它展示了：足够大规模的视频模型可以学到某些几何和物理规律。

需要重点学习：

- “patchified latent video” 这种表示方式。
- 如何跨时长、分辨率、宽高比训练。
- 长视频生成为什么会挑战物体恒常性、因果关系和时间一致性。
- 为什么“视频看起来很真实”不等于“仿真可靠”。

### 1.5 局限

Sora 这类模型可能生成视觉上合理的画面，但仍可能在这些方面失败：

- 精确物理因果。
- 长时间交互中的物体恒常性。
- 精确几何和接触动态。
- 动作可控的闭环仿真。

对自动驾驶或机器人来说，Sora 更像基础直觉和技术趋势，不是可以直接拿来做 log2world 的模拟器。

## 2. Cosmos

资料：

- NVIDIA, “Cosmos World Foundation Model Platform for Physical AI”: https://arxiv.org/abs/2501.03575
- NVIDIA Cosmos product page: https://www.nvidia.com/en-us/ai/cosmos/
- NVIDIA, “Cosmos 3: Omnimodal World Models for Physical AI”: https://arxiv.org/abs/2606.02800

### 2.1 问题

Cosmos 面向 Physical AI，包括机器人、自动驾驶、工业系统等需要理解、模拟和作用于物理世界的智能体。

它相对 Sora 的关键区别：

- Sora 主要是前沿视频生成模型，并带有 world simulation 的探索意味。
- Cosmos 更像一个为 Physical AI 构建定制化世界基础模型和合成数据流水线的平台。

### 2.2 Cosmos 1 / 平台视角

2025 年 Cosmos 平台包括：

- 视频数据清洗和整理 pipeline。
- 预训练 world foundation models。
- 视频 tokenizer。
- post-training 示例。
- 面向下游定制的开源 / 开权重组件。

它的思路是：先训练通用 world foundation model，再通过 fine-tuning / post-training 适配到具体任务。

### 2.3 Cosmos 3

Cosmos 3 走向 omnimodal world model。

输入和输出可以包括：

- 语言。
- 图像。
- 视频。
- 音频。
- 动作序列。

核心想法：

- 用统一的 mixture-of-transformers 架构处理和生成多种模态。
- 把 vision-language model、video generator、world simulator、world-action model 收进同一个框架。

### 2.4 为什么重要

Cosmos 重要在于：它不是只为媒体生成设计，而是直接面向 Physical AI 开发。

需要重点学习：

- world foundation model 和 video generator 的区别。
- 为什么数据清洗 / tokenization 和模型结构一样重要。
- post-training 如何把通用模型适配到机器人或自动驾驶。
- action、audio、language、video 如何统一到一个具身智能模型里。

### 2.5 和你方向的关系

Cosmos 和 DJI 岗位描述中的词非常接近：

- physical AI。
- world foundation model。
- synthetic data。
- simulation。
- action-conditioned generation。
- downstream fine-tuning。

如果想选一个工业相关性很强的系统深挖，Cosmos 是目前最适合作为锚点的工作之一。

## 3. GAIA

资料：

- GAIA-1 paper: https://arxiv.org/abs/2309.17080
- Wayve scaling GAIA-1 blog: https://wayve.ai/thinking/scaling-gaia-1/
- GAIA-2 paper: https://arxiv.org/html/2503.20523v1

### 3.1 问题

GAIA-1 是自动驾驶生成式世界模型。它希望在视频、文本和动作条件下，建模驾驶场景中可能出现的未来。

核心问题：

自动驾驶需要推理 counterfactual futures：如果自车采取不同动作，未来可能会怎样？

### 3.2 输入输出

输入：

- 视频上下文。
- 文本。
- 动作 / 自车行为信号。

输出：

- 真实感驾驶视频序列。
- 可控驾驶场景。

### 3.3 模型思想

GAIA-1 把 world modeling 看作无监督序列建模：

1. 把多模态输入映射成离散 token。
2. 预测序列中的下一个 token。
3. 通过 autoregressive prediction 生成未来驾驶场景。

它更像“驾驶 token 上的语言模型”，而不是纯 diffusion。

### 3.4 GAIA-2 方向

GAIA-2 进一步走向高分辨率、多相机驾驶场景生成，并加入更细粒度控制：

- Ego action。
- Agent behavior。
- Scene geometry。
- Environmental factors。

关键变化是：从单视角或有限控制，走向多视角、可控仿真。

### 3.5 应该学什么

GAIA 值得学习：

- tokenized world modeling。
- action-conditioned future prediction。
- counterfactual driving scenario generation。
- 自动驾驶世界模型中的 scaling effect。
- 为什么驾驶专用数据会让问题和通用视频生成不同。

### 3.6 局限

需要保持警惕的问题：

- 视频真实不保证轨迹物理合理。
- token-based prediction 可能难以保持精确几何。
- 动作可控性需要仔细评估：生成画面是真的服从动作，还是只是看起来合理？
- 多相机一致性非常难，并且是自动驾驶世界模型的核心问题。

## 4. DriveDreamer / DriveDreamer4D

资料：

- DriveDreamer paper: https://arxiv.org/abs/2309.09777
- DriveDreamer project page: https://drivedreamer.github.io/
- DriveDreamer4D paper: https://arxiv.org/abs/2410.13571

### 4.1 问题

DriveDreamer 关注 real-world-driven world models for autonomous driving。它希望生成的驾驶视频遵循真实交通约束，并支持未来预测或策略相关任务。

### 4.2 DriveDreamer 核心思想

DriveDreamer 使用带结构化交通条件的 diffusion modeling。

两阶段训练：

1. 学习结构化交通约束。
2. 学习 future-state prediction。

控制信号可以包括：

- 文本 prompt。
- 结构化交通条件。
- 驾驶动作。

输出：

- 可控驾驶视频。
- 未来驾驶场景预测。
- 某些设定下也包括驾驶动作预测。

### 4.3 DriveDreamer 和 GAIA 的区别

GAIA-1 更强调 video/text/action 上的 token sequence modeling。

DriveDreamer 更强调 structured traffic constraints 下的 diffusion generation。

简单说：

- GAIA：“预测未来驾驶 token。”
- DriveDreamer：“在结构化条件控制下生成驾驶视频。”

### 4.4 DriveDreamer4D

如果你关心 3DGS / 4DGS，DriveDreamer4D 特别值得看。

问题：

- 现有 NeRF / 3DGS 驾驶重建通常在训练轨迹附近表现好，但遇到换道、加速、减速等复杂 novel trajectory 时容易失败。
- Driving world model 可以生成多样视频，但 2D 视频缺少真实动态场景所需的时空一致性。

核心思路：

- 把 world model 当作 “data machine”，合成 novel-trajectory videos。
- 用结构化条件控制时空一致性。
- 用真实数据和合成 “cousin data” 混合训练或改进 4DGS。

需要重点学习：

- 视频生成先验如何改善 4D reconstruction。
- 合成数据如何扩展轨迹覆盖范围。
- 为什么 2D world model 和 4D scene representation 是互补关系。

这和你现在的思路很接近：用生成先验改进前馈重建，或者服务大幅度新视角外推。

## 5. Vista

资料：

- Vista paper: https://arxiv.org/abs/2405.17398
- Vista project page: https://opendrivelab.com/Vista/
- Vista official implementation: https://github.com/OpenDriveLab/Vista

### 5.1 问题

Vista 针对已有 driving world model 的三个弱点：

1. 对未见环境泛化差。
2. 关键细节保真度不足。
3. 动作可控性有限。

### 5.2 核心贡献

Vista 引入：

- 促进模型学习 moving instances 和 structural information 的 losses。
- latent replacement，把历史帧作为先验注入，从而稳定 long-horizon rollout。
- 多层级动作控制，从 high-level intention 到 low-level maneuver。

控制信号包括：

- Command。
- Goal point。
- Trajectory。
- Steering angle。
- Speed。

### 5.3 为什么 Vista 重要

Vista 是 action-conditioned driving world model 里非常清楚的一个样例。

它不是简单问“能不能生成驾驶视频”，而是问：

- 未来能不能被动作控制？
- 模型能否泛化到 open-world driving scenes？
- 长时间 rollout 能不能保持一致？
- 能不能在没有 ground-truth action 的情况下评估候选动作？

### 5.4 应该学什么

如果想理解 action-conditioned driving world model，Vista 可能是这组里最值得精读的论文之一。

阅读时重点看：

- 模型到底输入了哪些条件。
- action control 如何表示。
- long-horizon prediction 如何稳定。
- 如何鼓励 moving instances 和 structural information。
- 模型如何被用作 action selection 的 reward / evaluator。

### 5.5 和飞行 / 机器人场景的关系

对飞行或机器人场景来说，Vista 式问题会变成：

- action 应该如何表示？航点、速度、姿态、控制命令、轨迹？
- 模型如何保持场景布局和动态物体？
- 能不能通过生成未来来评估不同候选动作？

这是从 video generation 走向 planning 的概念桥梁。

## 6. WorldDreamer

资料：

- WorldDreamer paper: https://arxiv.org/abs/2401.09985
- WorldDreamer project page: https://world-dreamer.github.io/

### 6.1 问题

WorldDreamer 目标是更通用的 world model for video generation，不局限于驾驶或游戏。

它认为 world modeling 可以表述成无监督 visual sequence modeling。

### 6.2 核心思想

WorldDreamer：

1. 把视觉输入映射成离散 token。
2. 预测 masked tokens。
3. 使用 multimodal prompts 进行交互和控制。

它和 LLM 的类比很明确：

- 语言模型通过预测文本 token 学语言。
- WorldDreamer 试图通过预测视觉 token 学世界动态。

### 6.3 能力

报告中的任务包括：

- Text-to-video。
- Image-to-video。
- Video inpainting。
- Video stylization。
- Action-to-video。

### 6.4 应该学什么

WorldDreamer 适合理解 “general world model via token prediction” 这条路线。

关键问题：

- 把视觉动态离散化会带来什么收益和损失？
- masked token prediction 和 diffusion 相比有什么差异？
- multimodal prompt 如何进入模型？
- 通用视频建模能否迁移到驾驶或机器人这种专用任务？

### 6.5 局限

WorldDreamer 很宽，但宽也可能意味着精度不足。

对具身任务来说，关键缺口是：

- 强动作语义。
- 几何一致性。
- 闭环交互。
- 下游有效性的可靠评测。

## 7. Genie / Genie 2 / Genie 3

资料：

- Genie paper: https://arxiv.org/abs/2402.15391
- Genie project page: https://sites.google.com/view/genie-2024/home
- Genie 2 official blog: https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/
- Genie 3 official model page: https://deepmind.google/models/genie/
- Project Genie blog: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/

### 7.1 问题

Genie 面向 interactive environment generation。它问的是：

模型能不能从没有 ground-truth action label 的视频中，学习生成可玩的环境？

这和 Sora 不一样：

- Sora 生成视频。
- Genie 生成可以逐帧行动的环境。

### 7.2 Genie 1 核心架构

Genie 包括：

1. Spatiotemporal video tokenizer。
2. Latent action model。
3. Autoregressive dynamics model。

latent action model 是关键。

因为互联网视频通常没有动作标签，Genie 从视频转移中学习 latent action space。之后用户或智能体可以用这些 latent actions 在生成环境里行动。

### 7.3 Genie 2

Genie 2 走向从单张 prompt image 生成 action-controllable、playable 3D environments。

它的目标是训练和评估 embodied agents。

重要能力：

- 生成多样 3D 环境。
- 支持类似键鼠的控制。
- 当世界的一部分离开视野又重新进入视野时，仍保持一定世界一致性。

### 7.4 Genie 3

Genie 3 被描述为 general-purpose world model，可以从简单文本描述生成 interactive environments。它支撑 Project Genie，让用户创建、探索和 remix worlds。

这条线的领域变化是：

- 从被动视频生成；
- 到可交互世界生成；
- 再到具身智能体训练和评估。

### 7.5 应该学什么

Genie 是学习 latent action learning 的最佳案例。

重点看：

- 没有动作标签时，动作如何被学出来。
- 生成环境和生成视频有什么本质区别。
- 交互性如何改变评测问题。
- 它如何连接到机器人或自动驾驶仿真。

### 7.6 局限

需要思考：

- latent actions 能否和真实机器人 / 车辆控制动作语义对齐？
- 模型能保持多长时间的 coherent world state？
- 环境是否遵守物理，还是只是视觉合理？
- 能否 grounded 到真实传感器几何？

## 8. 横向对比

| 工作 | 领域 | 主要建模方式 | 控制方式 | 几何 / 物理 grounding | 最值得学的点 |
| --- | --- | --- | --- | --- | --- |
| Sora | 通用视频 | latent spacetime patches 上的 diffusion transformer | 文本 / 图像 / 视频 prompt | 涌现式，不显式 | 视频模型如何通过 scaling 逼近世界模拟 |
| Cosmos | Physical AI | world foundation model 平台，后续走向 omnimodal transformer | 语言 / 图像 / 视频 / 音频 / 动作 | 更强的 Physical AI 导向 | 工业级 world foundation model stack |
| GAIA | 自动驾驶 | 离散 token sequence modeling | 视频 / 文本 / 动作 | 驾驶领域，主要是视频层面 | action-conditioned driving future generation |
| DriveDreamer | 自动驾驶 | 带结构化交通约束的 diffusion | 文本 / 交通结构 / 动作 | 有结构约束，但主要仍是视频层面 | 可控真实驾驶视频生成 |
| DriveDreamer4D | 驾驶 4D 场景 | world model priors + 4DGS training | novel trajectories, structured conditions | 和 4D 表示结合更强 | 用生成视频改进 4D reconstruction |
| Vista | 自动驾驶 | 带动作控制和长 rollout 的 driving world model | command, goal, trajectory, steering angle, speed | 驾驶结构更强 | 可控高保真驾驶预测 |
| WorldDreamer | 通用视频 | 离散视觉 token / masked prediction | multimodal prompts, action-to-video | 宽泛但任务 grounding 较弱 | 通过 token prediction 学通用世界动态 |
| Genie | 可交互环境 | video tokenizer + latent action + autoregressive dynamics | learned latent actions / user control | 可交互，但不一定是 metric 3D | 从无标签视频中学习动作 |

## 9. 这个领域的主要技术张力

### 9.1 视频真实感 vs 世界正确性

高视觉真实感不够。用于规划或训练的 world model 必须保持：

- 因果一致性。
- 几何。
- 物体恒常性。
- 动作-响应正确性。
- 长时间世界状态。

Sora 和 WorldDreamer 更强在视觉生成；Vista、GAIA、DriveDreamer、Cosmos、Genie 更努力地往控制和实用性推进。

### 9.2 2D 生成 vs 3D/4D 表示

2D video model 很强，但容易 hallucinate geometry。

NeRF、3DGS、4DGS、occupancy、显式 scene graph 等 3D/4D 表示能提供更强结构，但更难 scale 和编辑。

最有希望的方向是 coupling：

- 用 3D/4D reconstruction 锚定几何。
- 用 generative model 填补未观测区域、长尾变化和照片级细节。
- 用生成数据反过来提升 reconstruction coverage。

这正是 DriveDreamer4D 值得认真看的原因。

### 9.3 开环生成 vs 闭环仿真

开环：

- 从 prompt 或历史帧生成视频。
- 评估视觉质量。

闭环：

- Agent 行动。
- 世界更新。
- Agent 再观察。
- 模型必须在重复交互下保持稳定。

Genie、Vista、Cosmos、GAIA 比普通 text-to-video 更接近这个方向。

### 9.4 数据和控制是真正的护城河

架构重要，但 world model 里常常更难的是：

- 整理高质量 multi-view / time / action 数据。
- 对齐 action、camera、scene 和 sensor signals。
- 设计对下游 agent 真正有用的控制信号。
- 评估合成数据是否真的提升训练。

## 10. 建议阅读顺序

### 阶段 1：建立概念底座

1. Sora technical report / blog。
2. Genie paper。
3. WorldDreamer paper。

目标：

- 理解为什么 video generation 被重新解释成 world modeling。
- 理解 video 的 patch / token 表示。
- 理解 latent action learning。

### 阶段 2：自动驾驶世界模型

4. GAIA-1。
5. DriveDreamer。
6. Vista。

目标：

- 理解 action-conditioned driving futures。
- 比较 token prediction、diffusion 和 controllable rollout。
- 学会看控制信号如何表示。

### 阶段 3：3D/4D 与 Physical AI

7. DriveDreamer4D。
8. Cosmos 2025 platform paper。
9. Cosmos 3 technical report。

目标：

- 理解 video world model 如何连接 4D reconstruction。
- 理解 world foundation model platform。
- 理解 Physical AI 数据流水线。

## 11. 和你当前研究方向的关系

你目前和这些工作最强的连接点是：

**通过 reconstruction-generation coupling 做大幅度新视角外推。**

技术上可以表述为：

- Feed-forward 3D reconstruction 提供几何和 camera-aware rendering。
- Generative model 为未观测内容和照片级修复提供先验。
- Synthetic / generated views 可以变成 reconstruction 的额外监督或质量约束。

和你最直接相关的论文：

1. DriveDreamer4D：生成先验改进 4DGS。
2. Vista：action-controllable driving world model。
3. Cosmos：Physical AI world foundation model platform。
4. GAIA-2：multi-view controllable driving world model。

建议一直追问的 thesis-level question：

> 能不能让 world model 足够几何 grounded，从而用于可控仿真，同时保留生成模型扩展长尾数据的灵活性？

## 12. 具体学习任务

每篇论文 / 系统都用这个模板填：

```text
论文：
领域：
输入：
输出：
控制信号：
表示方式：
训练目标：
数据集：
评测：
主要 claim：
真正证明了什么：
还没有证明什么：
和 reconstruction-generation coupling 的关系：
```

建议先做四个深挖：

1. Vista：画完整 conditioning / control pipeline。
2. DriveDreamer4D：画 generated novel-trajectory videos 如何改进 4DGS。
3. Genie：画从无标签视频中学习 latent action 的流程。
4. Cosmos：画 Physical AI WFM platform stack。

