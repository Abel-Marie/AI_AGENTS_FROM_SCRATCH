# AI Agents From Scratch

> A hands-on collection of AI-agent engineering examples built with **Google's Agent Development Kit (ADK)** — working through the core building blocks of production agent systems, one focused module at a time.

Each folder is a self-contained, runnable example that isolates one concept, from a single agent up to multi-agent coordination, tool use, evaluation, and observability.

## Modules

| Module | What it covers |
|--------|----------------|
| `simple_adk_agent/` | A minimal single agent — the starting point. |
| `adk_multi_agents/` | Coordinating multiple agents on one task. |
| `a2a_with_adk/` | **Agent-to-Agent (A2A)** communication with a client/server split. |
| `agent_tools/` | Giving agents tools — including **MCP** (`adk_mcp/`) and custom tools (`custom_tool/`). |
| `session_and_memory/` | Session state and agent memory across turns. |
| `agent_evaluation/` | Evaluating agent behavior against test data. |
| `agent_observability/` | Logging and tracing what an agent actually does. |

## Tech stack

`Python` · `google-adk` (Agent Development Kit) · `google-genai` (Gemini) · `mcp` (Model Context Protocol) · `python-dotenv`

## Setup

```bash
git clone https://github.com/Abel-Marie/AI_AGENTS_FROM_SCRATCH.git
cd AI_AGENTS_FROM_SCRATCH
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Add a `.env` with your Gemini key:

```
GOOGLE_API_KEY=your_key_here
```

Then run any module:

```bash
cd simple_adk_agent && python main.py
```

## Why this repo

Building each piece from scratch — multi-agent coordination, A2A, tool/MCP integration, evaluation, and observability — is how I learned the internals of reliable agent systems rather than just calling a framework.

## License

MIT
