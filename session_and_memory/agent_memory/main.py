import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the adk_session_memory root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from src.agents import create_memory_agent, create_agent_with_load_memory, create_auto_memory_agent
from src.utils import run_session

# Load enviroment variables
load_dotenv()

APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"

async def run_basic_memory_demo():
    print("\n--- Running Basic Memory Demo (Manual Save) ---")
    agent = create_memory_agent()
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    # 1. User tells agent about favorite color
    await run_session(
        runner,
        "My favorite color is blue-green. Can you write a Haiku about it?",
        "conversation-01",
    )
    
    # 2. Manually save session to memory
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
    )
    await memory_service.add_session_to_memory(session)
    print("✅ Session added to memory!")