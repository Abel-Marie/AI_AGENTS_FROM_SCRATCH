import os
import sys
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

# Add the agent_tools root to sys.path to allow imports from src as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.currency_agent import create_enhanced_currency_agent

# Load environment variables
load_dotenv()

def show_python_code_and_result(response):
    for i in range(len(response)):
        # Check if the response contains a valid function call result from the code executor
        if (
            (response[i].content.parts)
            and (response[i].content.parts[0])
            and (response[i].content.parts[0].function_response)
            and (response[i].content.parts[0].function_response.response)
        ):
            response_code = response[i].content.parts[0].function_response.response
            if "result" in response_code and response_code["result"] != "```":
                if "tool_code" in response_code["result"]:
                    print(
                        "Generated Python Code >> ",
                        response_code["result"].replace("tool_code", ""),
                    )
                else:
                    print("Generated Python Response >> ", response_code["result"])

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your GOOGLE_API_KEY.")
        return

    print("✅ Environment setup complete.")
    print("--- Running Enhanced Currency Agent ---")
    
    agent = create_enhanced_currency_agent()
    runner = InMemoryRunner(agent=agent)
    
    default_query = "Convert 1,250 USD to INR using a Bank Transfer. Show me the precise calculation."
    
    user_input = input(f"Enter your query (Press Enter for default: '{default_query}'): ").strip()
    query = user_input if user_input else default_query
    
    print(f"Running query: {query}")
    try:
        response = await runner.run_debug(query)
        show_python_code_and_result(response)
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
