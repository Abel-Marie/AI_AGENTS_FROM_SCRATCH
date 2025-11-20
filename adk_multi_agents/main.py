import os
import asyncio
import sys
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

# Import agent creators
from src.sequential.research_coordinator import create_research_coordinator
from src.sequential.blog_pipeline import create_blog_pipeline
from src.parallel.research_system import create_research_system
from src.loop.story_pipeline import create_story_pipeline

# Load environment variables
load_dotenv()

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your GOOGLE_API_KEY.")
        return

    print("✅ Environment setup complete.")
    
    while True:
        print("\nSelect an agent to run:")
        print("1. Research Coordinator (Sequential/Tool-use)")
        print("2. Blog Pipeline (Sequential)")
        print("3. Research System (Parallel)")
        print("4. Story Pipeline (Loop)")
        print("q. Quit")
        
        choice = input("Enter your choice (1-4 or q): ").strip()
        
        if choice.lower() == 'q':
            print("Exiting...")
            break

        runner = None
        query = ""
        agent_name = ""

        if choice == "1":
            agent_name = "Research Coordinator"
            agent = create_research_coordinator()
            runner = InMemoryRunner(agent=agent)
            default_query = "What are the latest advancements in quantum computing and what do they mean for AI?"
            
        elif choice == "2":
            agent_name = "Blog Pipeline"
            agent = create_blog_pipeline()
            runner = InMemoryRunner(agent=agent)
            default_query = "Write a blog post about the benefits of multi-agent systems for software developers"

        elif choice == "3":
            agent_name = "Research System"
            agent = create_research_system()
            runner = InMemoryRunner(agent=agent)
            default_query = "Run the daily executive briefing on Tech, Health, and Finance"

        elif choice == "4":
            agent_name = "Story Pipeline"
            agent = create_story_pipeline()
            runner = InMemoryRunner(agent=agent)
            default_query = "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map"
            
        else:
            print("Invalid choice. Please try again.")
            continue

        print(f"\n--- Running {agent_name} ---")
        user_input = input(f"Enter your query (Press Enter for default: '{default_query}'): ").strip()
        if user_input:
            query = user_input
        else:
            query = default_query

        if runner:
            print(f"Running query: {query}")
            try:
                response = await runner.run_debug(query)
            except Exception as e:
                print(f"❌ An error occurred: {e}")
            
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
