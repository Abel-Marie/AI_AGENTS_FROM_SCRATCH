# Sequential Agents

Sequential agents execute a series of sub-agents in a predefined linear order. The output of one agent typically serves as the context or input for the next agent in the chain.

## Use Cases
- **Content Pipelines**: Outline -> Draft -> Edit.
- **Data Processing**: Fetch -> Clean -> Analyze.
- **Step-by-Step Reasoning**: Decomposing a complex problem into logical steps.

## Examples in this Directory
- **`blog_pipeline.py`**: A classic content creation pipeline where an `OutlineAgent` creates a structure, a `WriterAgent` drafts the content, and an `EditorAgent` polishes the final result.
- **`research_coordinator.py`**: Demonstrates a coordinator agent that sequentially calls specific tools (which are themselves agents) to perform research and then summarization.
