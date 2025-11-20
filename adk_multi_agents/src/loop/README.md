# Loop Agents

Loop agents execute a sub-agent or a sequence of sub-agents repeatedly until a specific termination condition is met. This allows for iterative improvement and self-correction.

## Use Cases
- **Refinement Loops**: Draft -> Critique -> Refine (repeat until approved).
- **Code Generation**: Write Code -> Test -> Fix (repeat until tests pass).
- **Search & Explore**: Searching for information until a satisfactory answer is found.

## Examples in this Directory
- **`story_pipeline.py`**: Implements a "Story Refinement Loop". An `InitialWriterAgent` creates a draft, and then a `LoopAgent` cycles between a `CriticAgent` (who provides feedback) and a `RefinerAgent` (who improves the story). The loop continues until the critic outputs "APPROVED".
