# Parallel Agents

Parallel agents execute multiple sub-agents simultaneously. This is ideal for tasks where independent units of work can be performed concurrently to save time or gather diverse perspectives.

## Use Cases
- **Multi-Perspective Research**: Gathering information on different aspects of a topic (e.g., Tech, Health, Finance) at the same time.
- **Voting/Consensus**: Asking multiple agents to vote on a decision.
- **Independent Sub-tasks**: Generating different parts of a report that don't depend on each other.

## Examples in this Directory
- **`research_system.py`**: A system where three specialized researchers (`TechResearcher`, `HealthResearcher`, `FinanceResearcher`) gather information in parallel. Their outputs are then passed to an `AggregatorAgent` (running sequentially after the parallel block) to synthesize a final executive summary.
