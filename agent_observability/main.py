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

async def interactive_log_viewer():
    """Interactive log viewer with filtering and search."""
    log_file = "logger.log"
    if not os.path.exists(log_file):
        print("❌ No log file found. Run the broken agent first.")
        return

    while True:
        print("\n=== Interactive Log Viewer ===")
        print("1. View All Logs")
        print("2. View ERROR logs only")
        print("3. View INFO logs only")
        print("4. View DEBUG logs only")
        print("5. Search logs")
        print("6. Show errors with context")
        print("7. Back to main menu")
        
        choice = input("Select option (1-7): ").strip()
        
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if choice == "1":
            print(f"\n📋 All logs ({len(lines)} lines):")
            for line in lines[-50:]:  # Show last 50 lines
                print(line.rstrip())
            if len(lines) > 50:
                print(f"\n... ({len(lines) - 50} more lines above)")
                
        elif choice == "2":
            print("\n🔴 ERROR logs:")
            error_lines = [l for l in lines if "ERROR" in l]
            if error_lines:
                for line in error_lines:
                    print(line.rstrip())
            else:
                print("No ERROR logs found.")
                
        elif choice == "3":
            print("\n💡 INFO logs:")
            info_lines = [l for l in lines if "INFO" in l]
            for line in info_lines[-30:]:
                print(line.rstrip())
            if len(info_lines) > 30:
                print(f"\n... ({len(info_lines) - 30} more lines above)")
                
        elif choice == "4":
            print("\n🐛 DEBUG logs:")
            debug_lines = [l for l in lines if "DEBUG" in l]
            for line in debug_lines[-30:]:
                print(line.rstrip())
            if len(debug_lines) > 30:
                print(f"\n... ({len(debug_lines) - 30} more lines above)")
                
        elif choice == "5":
            keyword = input("Enter search keyword: ").strip()
            if keyword:
                print(f"\n🔍 Search results for '{keyword}':")
                results = [l for l in lines if keyword.lower() in l.lower()]
                if results:
                    for line in results:
                        print(line.rstrip())
                else:
                    print(f"No results found for '{keyword}'")
                    
        elif choice == "6":
            print("\n🎯 Errors with context (±3 lines):")
            error_indices = [i for i, l in enumerate(lines) if "ERROR" in l or "ValidationError" in l]
            if error_indices:
                for idx in error_indices:
                    start = max(0, idx - 3)
                    end = min(len(lines), idx + 4)
                    print(f"\n--- Context around line {idx + 1} ---")
                    for i in range(start, end):
                        prefix = ">>> " if i == idx else "    "
                        print(f"{prefix}{lines[i].rstrip()}")
            else:
                print("No errors found in logs.")
                
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

async def analyze_logs():
    """Simple log analysis - kept for backwards compatibility."""
    print("\n💡 Tip: Use the 'Interactive Log Viewer' for better analysis!")
    await interactive_log_viewer()

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
        print("2. Analyze Logs (Quick View)")
        print("3. Interactive Log Viewer (Detailed)")
        print("4. Run Fixed Agent (Reference Solution)")
        print("5. Challenge Mode (Fix it yourself)")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
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
            await interactive_log_viewer()
            
        elif choice == "4":
            print("\n--- Running Fixed Agent ---")
            query = input("Enter your research topic (or press Enter for default 'quantum computing'): ").strip()
            if not query:
                query = "Find recent papers on quantum computing"
            else:
                query = f"Find recent papers on {query}"
            
            agent = create_fixed_agent()
            await run_agent_debug(agent, query)
            
        elif choice == "5":
            await challenge_mode()
            
        elif choice == "6":
            print("Exiting...")
            cleanup_logs()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
