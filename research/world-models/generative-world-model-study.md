# Generative World Models Study Notes

Created: 2026-07-03

Scope: Sora, Cosmos, GAIA, DriveDreamer, Vista, WorldDreamer, Genie.

This note is for technical learning, not resume wording. The goal is to understand what each work is actually doing, how the methods differ, and how the field is moving from video generation toward controllable simulation and embodied-agent training.

## 0. What “world model” means here

In this reading group, a world model is not just a video generator. A useful world model should approximate how the world evolves under conditions or actions.

Useful axes:

1. **Prediction**: given past observations, predict plausible future observations.
2. **Control**: condition the future on action, trajectory, text, scene layout, camera pose, or other controls.
3. **Consistency**: preserve geometry, object identity, time, causality, and physical plausibility.
4. **Interactivity**: allow a human or agent to act in the generated environment step by step.
5. **Usefulness**: produce data or simulation that improves downstream agents, perception, planning, or evaluation.

The listed works form three families:

| Family | Works | Core idea |
| --- | --- | --- |
| General video/world simulators | Sora, WorldDreamer | Learn broad visual dynamics from web-scale videos/images; world modeling emerges through scale and temporal prediction. |
| Driving / physical AI world models | GAIA, DriveDreamer, Vista, Cosmos | Generate or predict driving/physical scenes with action, trajectory, scene, or sensor conditions. |
| Interactive environment generators | Genie | Generate playable environments, often learning latent actions from videos without explicit action labels. |

## 1. Sora

Sources:

- OpenAI, “Video generation models as world simulators”: https://openai.com/index/video-generation-models-as-world-simulators/
- OpenAI, “Sora: Creating video from text”: https://openai.com/index/sora/

### 1.1 Problem

Sora asks whether a large video generation model can become a simulator of the physical world. It is framed as text-conditioned video generation, but OpenAI explicitly describes the direction as learning to simulate the physical world in motion.

### 1.2 Inputs and outputs

Inputs:

- Text prompt.
- Still image prompt.
- Existing video for extension or completion.

Outputs:

- High-fidelity video with flexible duration, resolution, and aspect ratio.

### 1.3 Model idea

The key technical abstraction is to treat video and image data as sequences of spacetime patches in a latent space.

The rough pipeline:

1. Compress videos/images into latent codes.
2. Split latent codes into spacetime patches.
3. Use a transformer-based diffusion model over those patches.
4. Train jointly over images and videos with different aspect ratios, resolutions, and durations.

This is similar in spirit to language modeling: once all visual data become token-like patch sequences, scale and diversity become central.

### 1.4 Why it matters

Sora is important because it reframed video generation as a possible path toward world simulation. It is not driving-specific and does not expose a planning interface, but it shows that sufficiently scaled video models can learn some geometric and physical regularities.

What to learn from it:

- The “patchified latent video” representation.
- Scaling across durations/resolutions/aspect ratios.
- Why long video generation stresses object permanence, causality, and temporal consistency.
- Why impressive video generation is still not automatically reliable simulation.

### 1.5 Limitations to remember

Sora-like models can generate visually plausible scenes but may fail at:

- Exact physical causality.
- Object permanence under long interactions.
- Precise geometry and contact dynamics.
- Action-controllable closed-loop simulation.

For autonomous driving or robotics, Sora is more of a foundation intuition than a directly usable log2world simulator.

## 2. Cosmos

Sources:

- NVIDIA, “Cosmos World Foundation Model Platform for Physical AI”: https://arxiv.org/abs/2501.03575
- NVIDIA Cosmos product page: https://www.nvidia.com/en-us/ai/cosmos/
- NVIDIA, “Cosmos 3: Omnimodal World Models for Physical AI”: https://arxiv.org/abs/2606.02800

### 2.1 Problem

Cosmos targets Physical AI: robots, autonomous vehicles, industrial systems, and other agents that need to understand, simulate, and act in the physical world.

The key shift from Sora:

- Sora is mainly a frontier video generator with world-simulation aspirations.
- Cosmos is a platform for building customized world foundation models and synthetic data pipelines for physical AI.

### 2.2 Cosmos 1 / platform view

The 2025 Cosmos platform includes:

- Video curation pipeline.
- Pretrained world foundation models.
- Video tokenizers.
- Post-training examples.
- Open-weight/open-source components for downstream customization.

The philosophy is: train a general-purpose world foundation model, then fine-tune it into task-specific world models.

### 2.3 Cosmos 3

Cosmos 3 moves toward an omnimodal world model.

Inputs/outputs can include:

- Language.
- Image.
- Video.
- Audio.
- Action sequences.

Core idea:

- Use a unified mixture-of-transformers architecture to process and generate across modalities.
- Collapse vision-language models, video generators, world simulators, and world-action models into a single framework.

### 2.4 Why it matters

Cosmos is important because it is explicitly designed for physical AI development rather than only media generation.

What to learn:

- How a “world foundation model” differs from a video generator.
- Why data curation/tokenization matters as much as model architecture.
- How post-training adapts a generic model to robotics or autonomous driving.
- How action, audio, language, and video can be unified for embodied agents.

### 2.5 Relationship to your interests

Cosmos is close to the DJI JD vocabulary:

- physical AI,
- world foundation model,
- synthetic data,
- simulation,
- action-conditioned generation,
- downstream fine-tuning.

If you want to learn one industrially relevant system deeply, Cosmos is currently one of the best anchors.

## 3. GAIA

Sources:

- GAIA-1 paper: https://arxiv.org/abs/2309.17080
- Wayve scaling GAIA-1 blog: https://wayve.ai/thinking/scaling-gaia-1/
- GAIA-2 paper: https://arxiv.org/html/2503.20523v1

### 3.1 Problem

GAIA-1 is an autonomous-driving generative world model. It aims to model possible future outcomes in driving scenes, conditioned on video, text, and action.

The core problem:

Autonomous driving needs to reason about counterfactual futures: what could happen if the ego vehicle takes different actions?

### 3.2 Inputs and outputs

Inputs:

- Video context.
- Text.
- Action / ego-vehicle behavior signals.

Outputs:

- Realistic driving video sequences.
- Controllable driving scenarios.

### 3.3 Model idea

GAIA-1 casts world modeling as unsupervised sequence modeling:

1. Map multimodal inputs into discrete tokens.
2. Predict the next token in the sequence.
3. Generate future driving scenes by autoregressive prediction.

This is closer to “language modeling over driving tokens” than pure diffusion.

### 3.4 GAIA-2 direction

GAIA-2 advances toward high-resolution, multi-camera driving scene generation with finer controls:

- Ego actions.
- Agent behavior.
- Scene geometry.
- Environmental factors.

The important shift is from single-view or limited-control generation toward multi-view, controllable simulation.

### 3.5 What to learn

GAIA is worth reading for:

- Tokenized world modeling.
- Action-conditioned future prediction.
- Counterfactual driving scenario generation.
- Scaling effects in autonomous-driving world models.
- How domain-specific driving data changes the problem compared with general video generation.

### 3.6 Limitations

Potential limitations to think about:

- Video realism does not guarantee physically valid trajectories.
- Token-based prediction may struggle with precise geometry.
- Action controllability must be evaluated carefully: does the generated scene truly follow the action, or merely look plausible?
- Multi-camera consistency is hard and becomes central for autonomous driving.

## 4. DriveDreamer / DriveDreamer4D

Sources:

- DriveDreamer paper: https://arxiv.org/abs/2309.09777
- DriveDreamer project page: https://drivedreamer.github.io/
- DriveDreamer4D paper: https://arxiv.org/abs/2410.13571

### 4.1 Problem

DriveDreamer focuses on real-world-driven world models for autonomous driving. It wants generated driving video to respect real traffic constraints and support future prediction or policy-related tasks.

### 4.2 DriveDreamer core idea

DriveDreamer uses diffusion modeling with structured traffic conditions.

Two-stage training:

1. Learn structured traffic constraints.
2. Learn future-state prediction.

Controls can include:

- Text prompts.
- Structured traffic conditions.
- Driving actions.

Outputs:

- Controllable driving videos.
- Future driving scene predictions.
- In some formulations, driving action prediction.

### 4.3 Why DriveDreamer is different from GAIA

GAIA-1 emphasizes token sequence modeling over video/text/action.

DriveDreamer emphasizes diffusion generation under structured traffic constraints.

In simple terms:

- GAIA: “predict future driving tokens.”
- DriveDreamer: “generate driving video with structured controls.”

### 4.4 DriveDreamer4D

DriveDreamer4D is especially relevant if you care about 3DGS/4DGS.

Problem:

- Existing NeRF/3DGS driving reconstructions often work well near training trajectories but fail under complex novel trajectories such as lane changes or acceleration/deceleration.
- Driving world models can generate diverse videos, but 2D video lacks spatiotemporal coherence for real dynamic scenes.

Core idea:

- Use a world model as a “data machine” to synthesize novel-trajectory videos.
- Use structured conditions to control spatiotemporal consistency.
- Train or improve 4DGS using mixed real and synthetic “cousin data.”

What to learn:

- How video generation priors can improve 4D reconstruction.
- How synthetic data can expand trajectory coverage.
- Why 2D world models and 4D scene representations are complementary.

This is very close to your own current thinking: using generative priors to improve feed-forward reconstruction or large-baseline novel-view extrapolation.

## 5. Vista

Sources:

- Vista paper: https://arxiv.org/abs/2405.17398
- Vista project page: https://opendrivelab.com/Vista/
- Vista official implementation: https://github.com/OpenDriveLab/Vista

### 5.1 Problem

Vista targets three weaknesses of existing driving world models:

1. Poor generalization to unseen environments.
2. Insufficient fidelity for critical details.
3. Limited action controllability.

### 5.2 Core contributions

Vista introduces:

- Losses that promote learning moving instances and structural information.
- Latent replacement to inject historical frames as priors for coherent long-horizon rollouts.
- Multi-level action controls, from high-level intentions to low-level maneuvers.

Controls include:

- Command.
- Goal point.
- Trajectory.
- Steering angle.
- Speed.

### 5.3 Why Vista matters

Vista is one of the cleanest examples of a driving world model designed around controllability.

It is not just “generate driving video.” It asks:

- Can we control the future by action?
- Can the model generalize to open-world driving scenes?
- Can it roll out long horizons coherently?
- Can it evaluate candidate actions without ground-truth actions?

### 5.4 What to learn

Vista is probably the most useful paper in this list for understanding action-conditioned driving world models.

Focus when reading:

- What conditions are fed into the model.
- How action control is represented.
- How long-horizon prediction is stabilized.
- How moving instances and structural information are encouraged.
- How the model is used as a reward/evaluator for action selection.

### 5.5 Relationship to DJI-like roles

For flight or robot scenes, Vista-like questions become:

- How should action be represented? Waypoints, velocity, pose, control command, trajectory?
- How should the model preserve scene layout and moving objects?
- Can the model evaluate alternative actions through generated futures?

This is the conceptual bridge from video generation to planning.

## 6. WorldDreamer

Sources:

- WorldDreamer paper: https://arxiv.org/abs/2401.09985
- WorldDreamer project page: https://world-dreamer.github.io/

### 6.1 Problem

WorldDreamer aims at a more general world model for video generation, not limited to driving or games.

It argues that world modeling can be formulated as unsupervised visual sequence modeling.

### 6.2 Core idea

WorldDreamer:

1. Maps visual inputs into discrete tokens.
2. Predicts masked tokens.
3. Uses multimodal prompts for interaction and control.

The LLM analogy is explicit:

- Language models learn by predicting text tokens.
- WorldDreamer tries to learn world dynamics by predicting visual tokens.

### 6.3 Capabilities

Reported tasks include:

- Text-to-video.
- Image-to-video.
- Video inpainting.
- Video stylization.
- Action-to-video.

### 6.4 What to learn

WorldDreamer is useful for understanding the “general world model via token prediction” route.

Key questions:

- What does discretizing visual dynamics lose or gain?
- How does masked token prediction compare with diffusion?
- How do multimodal prompts enter the model?
- Does general video modeling transfer to specialized driving or robotics?

### 6.5 Limitations

WorldDreamer is broad, but broadness can weaken precision.

For embodied tasks, the important missing pieces are:

- Strong action semantics.
- Geometry-aware consistency.
- Closed-loop interaction.
- Reliable evaluation of downstream usefulness.

## 7. Genie / Genie 2 / Genie 3

Sources:

- Genie paper: https://arxiv.org/abs/2402.15391
- Genie project page: https://sites.google.com/view/genie-2024/home
- Genie 2 official blog: https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/
- Genie 3 official model page: https://deepmind.google/models/genie/
- Project Genie blog: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/

### 7.1 Problem

Genie targets interactive environment generation. It asks:

Can a model learn to generate playable environments from videos without ground-truth action labels?

This is different from Sora:

- Sora generates videos.
- Genie generates environments that can be acted in frame by frame.

### 7.2 Genie 1 core architecture

Genie consists of:

1. Spatiotemporal video tokenizer.
2. Latent action model.
3. Autoregressive dynamics model.

The latent action model is the key idea.

Because internet videos usually do not contain action labels, Genie learns a latent action space from video transitions. Users or agents can then act in the generated environment using these latent actions.

### 7.3 Genie 2

Genie 2 moves to action-controllable, playable 3D environments from a single prompt image.

It is intended for training and evaluating embodied agents.

Important abilities:

- Generate diverse 3D environments.
- Support keyboard/mouse-like control.
- Maintain some world consistency when parts of the world leave and re-enter view.

### 7.4 Genie 3

Genie 3 is described as a general-purpose world model that generates interactive environments from simple text descriptions. It powers Project Genie, where users can create, explore, and remix worlds.

The key field-level move:

- From passive video generation,
- to interactive world generation,
- to embodied-agent training and evaluation.

### 7.5 What to learn

Genie is the best case study for latent action learning.

Focus on:

- How actions can be learned without labels.
- How a generated environment differs from a generated video.
- How interactivity changes the evaluation problem.
- How this could connect to robotics or autonomous-driving simulation.

### 7.6 Limitations

Questions to keep in mind:

- Are latent actions semantically aligned with real robot/control actions?
- How long can the model maintain a coherent world state?
- Does the environment obey physics or only visual plausibility?
- Can it be grounded to real sensor geometry?

## 8. Cross-paper comparison

| Work | Domain | Main modeling style | Control | Geometry / physical grounding | Best learning value |
| --- | --- | --- | --- | --- | --- |
| Sora | General video | Diffusion transformer over spacetime latent patches | Text/image/video prompts | Emergent, not explicit | Scaling video models as simulators |
| Cosmos | Physical AI | World foundation model platform; later omnimodal transformers | Language/image/video/audio/action | Stronger physical-AI orientation | Industrial world foundation model stack |
| GAIA | Autonomous driving | Discrete token sequence modeling | Video/text/action | Driving-specific, video-level | Action-conditioned driving future generation |
| DriveDreamer | Autonomous driving | Diffusion with structured traffic constraints | Text, traffic structure, action | Structured but mainly video-level | Controlled real-world driving video generation |
| DriveDreamer4D | Driving 4D scenes | World model priors + 4DGS training | Novel trajectories, structured conditions | Stronger 4D representation link | Using generated videos to improve 4D reconstruction |
| Vista | Autonomous driving | Driving world model with action controls and long rollout | Command, goal, trajectory, angle, speed | Stronger driving-structure focus | Controllable high-fidelity driving prediction |
| WorldDreamer | General video | Discrete visual token modeling / masked prediction | Multimodal prompts, action-to-video | Broad but less task-grounded | General world dynamics via token prediction |
| Genie | Interactive environments | Video tokenizer + latent action + autoregressive dynamics | Learned latent actions / user control | Interactive but not necessarily metric 3D | Learning actions from unlabeled videos |

## 9. The field’s main technical tension

### 9.1 Video realism vs world correctness

High visual fidelity is not enough. A world model used for planning or training must preserve:

- Causal consistency.
- Geometry.
- Object permanence.
- Action-response correctness.
- Long-horizon state.

Sora and WorldDreamer are strong on visual generation; Vista, GAIA, DriveDreamer, Cosmos, and Genie push harder toward control and utility.

### 9.2 2D generation vs 3D/4D representation

2D video models are powerful but may hallucinate geometry.

3D/4D representations such as NeRF, 3DGS, 4DGS, occupancy, or explicit scene graphs provide stronger structure but are harder to scale and edit.

The most promising direction is coupling:

- Use 3D/4D reconstruction to anchor geometry.
- Use generative models to fill unobserved regions, long-tail variation, and photorealistic detail.
- Use generated data to improve reconstruction coverage.

This is exactly why DriveDreamer4D is a useful paper to read carefully.

### 9.3 Open-loop generation vs closed-loop simulation

Open-loop:

- Generate a video from a prompt or past frames.
- Evaluate visual quality.

Closed-loop:

- Agent acts.
- World updates.
- Agent observes again.
- The model must remain stable under repeated interaction.

Genie, Vista, Cosmos, and GAIA are more relevant to this direction than plain text-to-video models.

### 9.4 Dataset and control are the real moat

Architecture matters, but in world models the hard part is often:

- Curating high-quality multi-view/time/action data.
- Aligning action, camera, scene, and sensor signals.
- Designing controls that are useful for downstream agents.
- Evaluating whether synthetic data improves training.

## 10. Suggested reading order

### Stage 1: build the conceptual base

1. Sora technical report/blog.
2. Genie paper.
3. WorldDreamer paper.

Goal:

- Understand why video generation is being reframed as world modeling.
- Understand patch/token views of video.
- Understand latent action learning.

### Stage 2: autonomous-driving world models

4. GAIA-1.
5. DriveDreamer.
6. Vista.

Goal:

- Understand action-conditioned driving futures.
- Compare token prediction, diffusion, and controllable rollout.
- Learn how control signals are represented.

### Stage 3: 3D/4D and physical AI

7. DriveDreamer4D.
8. Cosmos 2025 platform paper.
9. Cosmos 3 technical report.

Goal:

- Understand how video world models connect to 4D reconstruction.
- Understand world foundation model platforms.
- Understand physical-AI data pipelines.

## 11. Notes for your own research direction

Your current strongest bridge to these works is:

**large-baseline novel-view extrapolation through reconstruction-generation coupling.**

This can be phrased technically as:

- Feed-forward 3D reconstruction provides geometry and camera-aware rendering.
- Generative models provide priors for unobserved content and photorealistic repair.
- Synthetic/generated views can become extra supervision or quality constraints for reconstruction.

The most directly relevant papers for you:

1. DriveDreamer4D: generation priors improve 4DGS.
2. Vista: action-controllable driving world model.
3. Cosmos: physical-AI foundation model platform.
4. GAIA-2: multi-view controllable driving world model.

The best “thesis-level” question to keep asking:

> Can we make world models geometrically grounded enough for controllable simulation, while keeping the generative flexibility needed for long-tail data expansion?

## 12. Concrete study tasks

For each paper/system, fill in this template:

```text
Paper:
Domain:
Input:
Output:
Control signal:
Representation:
Training objective:
Dataset:
Evaluation:
Main claim:
What is actually proven:
What remains unproven:
How it relates to reconstruction-generation coupling:
```

Recommended first deep-dive:

1. Vista: draw the complete conditioning/control pipeline.
2. DriveDreamer4D: draw how generated novel-trajectory videos improve 4DGS.
3. Genie: draw latent-action learning from unlabeled video.
4. Cosmos: draw the physical-AI WFM platform stack.

