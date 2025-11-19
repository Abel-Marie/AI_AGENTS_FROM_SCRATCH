# Simple Google ADK Agent

This project is a simple, asynchronous AI agent built using Python and what appears to be a custom implementation related to Google's Agent Development Kit (ADK). It demonstrates the basic setup for creating an agent runner, loading environment variables for API keys, and executing a query.

## 🚀 Features

- **Asynchronous:** Built with Python's `asyncio` for efficient I/O operations.
- **Environment-based Configuration:** Securely manages API keys using a `.env` file.
- **Simple Agent Runner:** A clear example of how to initialize and run a query with an agent.

##📋 Prerequisites

- Python 3.7+
- A Google API Key with access to the Gemini API (or the relevant Google AI service).

## ⚙️ Setup and Installation

Follow these steps to get the project up and running on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd simple_adk_agent
    ```

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    You'll need to create a `requirements.txt` file. Based on the project, it should contain:
    ```
    # requirements.txt
    python-dotenv
    google-generativeai
    ```
    Install these packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a file named `.env` in the root of the project directory. This file will store your secret API key.

    ```
    # .env
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
    ```
    Replace `"YOUR_GOOGLE_API_KEY_HERE"` with your actual Google API key.

## ▶️ How to Run

Once the setup is complete, you can run the agent by executing the `main.py` script:

```bash
python main.py
```

The script will:
1.  Load your `GOOGLE_API_KEY` from the `.env` file.
2.  Create an agent runner.
3.  Execute a hardcoded query: *"What is Agent Development Kit from Google? What languages is the SDK available in?"*
4.  Print the agent's response to the console.

## 📂 Project Structure

```
simple_adk_agent/
├── src/
│   └── agent.py      # Contains the agent creation logic (create_runner)
├── .env              # Stores environment variables (you need to create this)
├── main.py           # Main script to run the agent
├── requirements.txt  # Project dependencies (you may need to create this)
└── README.md         # This file
```