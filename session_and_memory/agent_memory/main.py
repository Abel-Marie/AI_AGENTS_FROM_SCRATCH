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

async def run_search_demo():
    print("\n--- Running Search Memory Demo ---")
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    # Populate memory
    temp_agent = create_memory_agent()
    temp_runner = Runner(agent=temp_agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)
    await run_session(temp_runner, "My favorite color is blue.", "color-session")
    session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id="color-session")
    await memory_service.add_session_to_memory(session)
    
    # Search
    print("\nSearching for 'favorite color'...")
    search_response = await memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query="What is the user's favorite color?"
    )

    print("🔍 Search Results:")
    print(f"  Found {len(search_response.memories)} relevant memories")
    for memory in search_response.memories:
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"  [{memory.author}]: {text}...")

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please ensure .env file exists in adk_session_memory/ with GOOGLE_API_KEY.")
        return

    while True:
        print("\n=== ADK Memory Project ===")
        print("1. Basic Memory (Manual Save)")
        print("2. Retrieval Demo (load_memory)")
        print("3. Auto-Save Demo")
        print("4. Search Memory Demo")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            await run_basic_memory_demo()
        elif choice == "2":
            await run_retrieval_demo()
        elif choice == "3":
            await run_auto_save_demo()
        elif choice == "4":
            await run_search_demo()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())

