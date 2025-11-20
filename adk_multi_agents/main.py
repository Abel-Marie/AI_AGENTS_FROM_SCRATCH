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
    print("Select an agent to run:")
    print("1. Research Coordinator (Sequential/Tool-use)")
    print("2. Blog Pipeline (Sequential)")
    print("3. Research System (Parallel)")
    print("4. Story Pipeline (Loop)")

    