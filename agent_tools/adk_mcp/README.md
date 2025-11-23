# ADK MCP Agent Tools

This project demonstrates how to use the Agent Development Kit (ADK) with the Model Context Protocol (MCP).

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r ../../requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory (`AI_AGENTS_FROM_SCRATCH`) or in this directory with your Google API key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

3.  **Install Node.js & npx**:
    Ensure you have Node.js installed, as the MCP tools use `npx`.

## Usage

Run the main script to access the interactive menu:

```bash
python main.py
```

## Demos

1.  **Image Agent Demo (MCP)**: Uses the `@modelcontextprotocol/server-everything` to generate a tiny image.
2.  **Shipping Agent Demo (Human-in-the-loop)**: Demonstrates a shipping workflow with human approval for large orders.
