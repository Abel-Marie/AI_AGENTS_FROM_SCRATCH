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

async def run_retrieval_demo():
    print("\n--- Running Retrieval Demo (load_memory) ---")
    # We need a memory service with some data. Let's populate it first.
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    # Pre-populate memory
    print("Populating memory with birthday info...")
    temp_agent = create_memory_agent()
    temp_runner = Runner(agent=temp_agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)
    await run_session(temp_runner, "My birthday is on March 15th.", "birthday-session-01")
    birthday_session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id="birthday-session-01")
    await memory_service.add_session_to_memory(birthday_session)
    print("✅ Birthday session saved to memory!")

    # Now use agent with load_memory
    agent = create_agent_with_load_memory()
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    # Ask about birthday in a NEW session
    await run_session(runner, "When is my birthday?", "birthday-session-02")

async def run_auto_save_demo():
    print("\n--- Running Auto-Save Demo ---")
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    agent = create_auto_memory_agent()
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    # 1. Tell agent about a gift (auto-saved)
    await run_session(
        runner,
        "I gifted a new toy to my nephew on his 1st birthday!",
        "auto-save-test",
    )
    print("✅ Turn completed (and auto-saved).")

    # 2. Ask about the gift in a NEW session
    await run_session(
        runner,
        "What did I gift my nephew?",
        "auto-save-test-2",
    )