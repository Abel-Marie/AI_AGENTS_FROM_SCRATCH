from google.genai import types
from google.adk.runners import Runner

async def run_session(
    runner_instance: Runner, user_queries: list[str] | str, session_id: str = "default", app_name: str = "MemoryDemoApp", user_id: str = "demo_user"
):
    """Helper function to run queries in a session and display responses."""
    print(f"\n### Session: {session_id}")

    session_service = runner_instance.session_service

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

