import os
import asyncio
from dotenv import load_dotenv
from src.agent import create_runner

# Load enviroment variable
load_dotenv()

load_dotenv()

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print(" Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your GOOGLE_API_KEY.")
        return

    print("Environment setup complete.")

    try:
        runner = create_runner()
        print(" Runner created.")
        
        query = "What is Agent Development Kit from Google? What languages is the SDK available in?"
        print(f"Running query: {query}")
        
        response = await runner.run_debug(query)
        
    except Exception as e:
        print(f" An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
