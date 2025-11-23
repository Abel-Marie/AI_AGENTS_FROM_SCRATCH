import sqlite3
from google.genai import types
from google.adk.runners import Runner 

async def run_session(
        runner_instance: Runner,
        user_queries: list[str] | str = None,
        session_name: str = "default",
        user_id: str = "default",
        model_name: str = "gemini-2.5-flash-lite",
): 

