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
        
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
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

async def step_by_step_debug_guide():
    """Interactive step-by-step debugging tutorial."""
    print("\n" + "="*60)
    print("🎓 STEP-BY-STEP DEBUG GUIDE")
    print("="*60)
    print("\nYou'll learn how to debug a type mismatch error in the agent.")
    input("\nPress Enter to start...")
    
    # Step 1: Run and observe failure
    print("\n" + "-"*60)
    print("📍 STEP 1: Run the Broken Agent and Observe the Failure")
    print("-"*60)
    print("\nFirst, let's run the broken agent to see what happens.")
    print("This will generate logs that we can analyze.")
    
    choice = input("\nRun broken agent now? (y/n): ").strip().lower()
    if choice == 'y':
        agent = create_broken_agent()
        await run_agent_debug(agent, "Find recent papers on AI safety")
        print("\n❌ The agent failed! Let's find out why.")
    
    input("\nPress Enter to continue to Step 2...")
    
    # Step 2: Analyze the stack trace
    print("\n" + "-"*60)
    print("📍 STEP 2: Analyze the Stack Trace")
    print("-"*60)
    print("\nLet's look at the ERROR logs to understand what went wrong.")
    print("\n💡 Key Question: What type of error do you see?")
    print("   (Look for words like 'ValidationError', 'TypeError', etc.)")
    
    log_file = "logger.log"
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        
        error_lines = [l for l in lines if "ERROR" in l or "ValidationError" in l]
        if error_lines:
            print("\n🔴 Error found:")
            for line in error_lines[:3]:  # Show first 3 errors
                print(f"   {line.strip()}")
    
    input("\nPress Enter to continue to Step 3...")
    
    # Step 3: Identify the type mismatch
    print("\n" + "-"*60)
    print("📍 STEP 3: Identify the Type Mismatch")
    print("-"*60)
    print("\n🔍 Analysis:")
    print("   The error says: 'Expected type List[str] but got str'")
    print("\n💡 This means:")
    print("   - The function expects a LIST of strings: ['paper1', 'paper2']")
    print("   - But it's receiving a SINGLE string: 'paper1'")
    print("\n📝 Location:")
    print("   - File: agent_observability/src/broken_agent.py")
    print("   - Function: count_papers()")
    
    input("\nPress Enter to continue to Step 4...")
    
    # Step 4: Examine the code
    print("\n" + "-"*60)
    print("📍 STEP 4: Examine the Code")
    print("-"*60)
    print("\nLet's look at the broken code:")
    print("\n" + "─"*50)
    print("def count_papers(papers: str):  # ❌ WRONG!")
    print("    '''")
    print("    Counts the number of papers.")
    print("    Args:")
    print("        papers: A list of strings  # ← Says 'list' in docs")
    print("    '''")
    print("    return len(papers)")
    print("─"*50)
    print("\n🤔 Do you see the problem?")
    print("   - Type hint says: papers: str (a single string)")
    print("   - Documentation says: 'A list of strings'")
    print("   - There's a MISMATCH!")
    
    input("\nPress Enter to continue to Step 5...")
    
    # Step 5: Apply the fix
    print("\n" + "-"*60)
    print("📍 STEP 5: Apply the Fix")
    print("-"*60)
    print("\n✅ The correct code should be:")
    print("\n" + "─"*50)
    print("from typing import List")
    print("")
    print("def count_papers(papers: List[str]):  # ✅ CORRECT!")
    print("    '''")
    print("    Counts the number of papers.")
    print("    Args:")
    print("        papers: A list of strings")
    print("    '''")
    print("    return len(papers)")
    print("─"*50)
    print("\n📚 Key Lesson:")
    print("   Type hints must match the actual data type!")
    print("   The agent uses type hints to validate function calls.")
    
    input("\nPress Enter to see the summary...")
    
    # Summary
    print("\n" + "="*60)
    print("🎉 DEBUGGING COMPLETE!")
    print("="*60)
    print("\n📖 What You Learned:")
    print("   1. How to run an agent and observe failures")
    print("   2. How to read error logs and stack traces")
    print("   3. How to identify type mismatch errors")
    print("   4. How to fix type hints in Python")
    print("   5. Why type safety matters in AI agents")
    print("\n💡 Next Step:")
    print("   Run the 'Fixed Agent' option to see the correct implementation!")
    
async def challenge_mode():
    """Quick challenge - redirects to step-by-step guide."""
    print("\n💡 For a better learning experience, use the Step-by-Step Guide!")
    choice = input("Start the Step-by-Step Debug Guide? (y/n): ").strip().lower()
    if choice == 'y':
        await step_by_step_debug_guide()
    else:
        print("\n⚔️  QUICK CHALLENGE")
        print("1. Open 'agent_observability/src/broken_agent.py'")
        print("2. Find the 'count_papers' function")
        print("3. Change: papers: str → papers: List[str]")
        print("4. Add: from typing import List")
        input("\nPress Enter when done...")

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
        print("4. Step-by-Step Debug Guide (Tutorial)")
        print("5. Run Fixed Agent (Reference Solution)")
        print("6. Challenge Mode (Quick Fix)")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
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
            await step_by_step_debug_guide()
            
        elif choice == "5":
            print("\n--- Running Fixed Agent ---")
            query = input("Enter your research topic (or press Enter for default 'quantum computing'): ").strip()
            if not query:
                query = "Find recent papers on quantum computing"
            else:
                query = f"Find recent papers on {query}"
            
            agent = create_fixed_agent()
            await run_agent_debug(agent, query)
            
        elif choice == "6":
            await challenge_mode()
            
        elif choice == "7":
            print("Exiting...")
            cleanup_logs()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
