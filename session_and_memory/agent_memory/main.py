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

    print("Step 1: Chat with the agent (e.g., tell it your favorite color).")
    await run_session(
        runner,
        session_id="conversation-01",
        interactive=True
    )
    
    # 2. Manually save session to memory
    print("\nSaving session to memory...")
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
    )
    await memory_service.add_session_to_memory(session)
    print("✅ Session added to memory!")

async def run_retrieval_demo():
    print("\n--- Running Retrieval Demo (load_memory) ---")
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    # Pre-populate memory
    print("Populating memory with birthday info (March 15th)...")
    temp_agent = create_memory_agent()
    temp_runner = Runner(agent=temp_agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)
    await run_session(temp_runner, "My birthday is on March 15th.", "birthday-session-01")
    birthday_session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id="birthday-session-01")
    await memory_service.add_session_to_memory(birthday_session)
    print("✅ Birthday session saved to memory!")

    # Now use agent with load_memory
    print("\nNow, ask the agent about your birthday in a NEW session.")
    agent = create_agent_with_load_memory()
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

    await run_session(runner, session_id="birthday-session-02", interactive=True)

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

    print("Step 1: Tell the agent something (it will be auto-saved).")
    await run_session(
        runner,
        session_id="auto-save-test",
        interactive=True
    )
    print("✅ Session ended (and auto-saved).")

    print("\nStep 2: Start a new session and ask about what you said.")
    await run_session(
        runner,
        session_id="auto-save-test-2",
        interactive=True
    )

async def run_search_demo():
    print("\n--- Running Search Memory Demo ---")
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    # Populate memory
    print("Populating memory with favorite color (blue)...")
    temp_agent = create_memory_agent()
    temp_runner = Runner(agent=temp_agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)
    await run_session(temp_runner, "My favorite color is blue.", "color-session")
    session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id="color-session")
    await memory_service.add_session_to_memory(session)
    
    # Search
    print("\nType a query to search your memory (e.g., 'favorite color').")
    query = input("Search Query > ").strip()
    
    search_response = await memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query=query
    )

    print("🔍 Search Results:")
    print(f"  Found {len(search_response.memories)} relevant memories")
    for memory in search_response.memories:
        if memory.content and memory.content.parts:
            text = memory.content.parts[0].text[:80]
            print(f"  [{memory.author}]: {text}...")

async def run_memory_explorer():
    print("\n--- Memory Explorer ---")
    print("This tool lets you inspect all memories stored in the vector database.")
    
    # We use a persistent memory service for this demo to see 'real' data if we had it,
    # but for this in-memory demo, we'll just use the in-memory one which is empty 
    # unless we populate it in this run. 
    # To make it useful, let's populate some dummy data if empty.
    
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    # Check if empty (hacky check for demo)
    # In a real app, we'd connect to a real DB.
    print("Populating some sample memories for exploration...")
    temp_agent = create_memory_agent()
    temp_runner = Runner(agent=temp_agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)
    
    facts = [
        "The capital of France is Paris.",
        "Python is a popular programming language.",
        "The speed of light is approximately 299,792 km/s."
    ]
    
    for i, fact in enumerate(facts):
        await run_session(temp_runner, fact, f"fact-session-{i}")
        session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=f"fact-session-{i}")
        await memory_service.add_session_to_memory(session)
        
    print("✅ Sample memories added.")
    
    while True:
        print("\nOptions:")
        print("1. Search Memory")
        print("2. Back to Main Menu")
        choice = input("Explorer > ").strip()
        
        if choice == "1":
            query = input("Search Query > ").strip()
            search_response = await memory_service.search_memory(
                app_name=APP_NAME, user_id=USER_ID, query=query
            )
            print(f"Found {len(search_response.memories)} results:")
            for mem in search_response.memories:
                 if mem.content and mem.content.parts:
                    print(f" - {mem.content.parts[0].text}")
        elif choice == "2":
            break

async def run_teach_agent_game():
    print("\n--- Teach the Agent Game ---")
    print("Goal: Teach the agent 3 facts, then quiz it!")
    
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    agent = create_auto_memory_agent() # Use auto-save for smoother flow
    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service, memory_service=memory_service)
    
    print("\nPhase 1: Teaching")
    print("Tell the agent 3 distinct facts (e.g., 'My dog's name is Rex').")
    
    for i in range(1, 4):
        print(f"\nFact {i}:")
        await run_session(runner, session_id=f"teaching-session-{i}", interactive=True)
        
    print("\nPhase 2: Quizzing")
    print("Now, start a new session and ask the agent about what you taught it.")
    await run_session(runner, session_id="quiz-session", interactive=True)
    
    print("\n✅ Game Over! Did the agent remember?")

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please ensure .env file exists in adk_session_memory/ with GOOGLE_API_KEY.")
        return

    while True:
        print("\n=== ADK Memory Project (Interactive) ===")
        print("1. Basic Memory (Manual Save)")
        print("2. Retrieval Demo (load_memory)")
        print("3. Auto-Save Demo")
        print("4. Search Memory Demo")
        print("5. Memory Explorer ")
        print("6. Teach the Agent Game")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            await run_basic_memory_demo()
        elif choice == "2":
            await run_retrieval_demo()
        elif choice == "3":
            await run_auto_save_demo()
        elif choice == "4":
            await run_search_demo()
        elif choice == "5":
            await run_memory_explorer()
        elif choice == "6":
            await run_teach_agent_game()
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
