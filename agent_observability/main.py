import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the agent_observability root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.logger import setup_logging, cleanup_logs
from src.broken_agent import create_broken_agent
from src.fixed_agent import create_fixed_agent
from src.utils import run_agent_debug

# Load environment variables
load_dotenv()

async def analyze_logs():
    """Reads the log file and highlights errors."""
    log_file = "logger.log"
    if not os.path.exists(log_file):
        print("❌ No log file found. Run the broken agent first.")
        return

    print(f"\n🔍 Analyzing {log_file}...")
    with open(log_file, "r") as f:
        lines = f.readlines()
        
    error_found = False
    for line in lines:
        if "ERROR" in line or "Traceback" in line or "ValidationError" in line:
            print(f"🔴 {line.strip()}") # Highlight error
            error_found = True
        elif "DEBUG" in line:
            # Print debug lines in grey/dim if possible, or just normal
            # For simplicity in standard terminal:
            pass 
    
    if error_found:
        print("\n💡 Analysis: Errors detected in the logs.")
        print("   Look for 'ValidationError' or type mismatches.")
        print("   The agent might be passing a 'str' where a 'list' is expected.")
    else:
        print("✅ No obvious errors found in the logs (or debug level too low).")

async def challenge_mode():
    """Guided challenge to fix the bug."""
    print("\n⚔️  CHALLENGE MODE ⚔️")
    print("1. Open 'agent_observability/src/broken_agent.py'")
    print("2. Find the 'count_papers' function.")
    print("3. Identify why it fails (Hint: Check the type hint of 'papers').")
    print("4. Fix the code!")
    
    input("\nPress Enter once you have fixed the code...")
    
    print("\nRunning the agent with YOUR fix...")
    # Reload the module to pick up changes (simplified for this demo, usually requires importlib)
    # Since we can't easily hot-reload in this simple script structure without complexity,
    # we'll just re-import or warn the user.
    print("⚠️  Note: For the fix to take effect in this running process, we would need to reload modules.")
    print("   Please restart 'main.py' and select 'Run Broken Agent' (which should now be fixed) to verify.")
    print("   Or, run the 'Fixed Agent' option to see the reference solution.")

async def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your GOOGLE_API_KEY.")
        return

    setup_logging()

    while True:
        print("\n=== Agent Observability & Debugging ===")
        print("1. Run Broken Agent (Expect Failure)")
        print("2. Analyze Logs (Find the Bug)")
        print("3. Run Fixed Agent (Reference Solution)")
        print("4. Challenge Mode (Fix it yourself)")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\n--- Running Broken Agent ---")
            query = input("Enter your research topic (or press Enter for default 'quantum computing'): ").strip()
            if not query:
                query = "Find recent papers on quantum computing"
            else:
                query = f"Find recent papers on {query}"
            
            agent = create_broken_agent()
            await run_agent_debug(agent, query)
            print("\n❌ Agent failed? Good! Now check the logs.")
            
        elif choice == "2":
            await analyze_logs()
            
        elif choice == "3":
            print("\n--- Running Fixed Agent ---")
            query = input("Enter your research topic (or press Enter for default 'quantum computing'): ").strip()
            if not query:
                query = "Find recent papers on quantum computing"
            else:
                query = f"Find recent papers on {query}"
            
            agent = create_fixed_agent()
            await run_agent_debug(agent, query)
            
        elif choice == "4":
            await challenge_mode()
            
        elif choice == "5":
            print("Exiting...")
            cleanup_logs()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
