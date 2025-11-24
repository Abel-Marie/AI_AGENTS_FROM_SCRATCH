from google.genai import types
from google.adk.runners import Runner

async def run_session(
    runner_instance: Runner, user_queries: list[str] | str, session_id: str = "default", app_name: str = "MemoryDemoApp", user_id: str = "demo_user"
):