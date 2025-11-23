import os
import asyncio
from dotenv import load_dotenv

from src.image_agent import run_image_demo
from src.shipping_agent import run_shipping_demos

# Load environment variables
load_dotenv()

async def main():
    """Main function to run the ADK MCP Project demos."""
    # Try loading from current directory if not found
    if not os.getenv("GOOGLE_API_KEY"):
        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
        print("Please create a .env file with your GOOGLE_API_KEY.")
        return

    print("✅ Environment setup complete.")
    
    while True:
        print("\n--- ADK MCP Project Menu ---")
        print("1. Run Image Agent Demo (MCP)")
        print("2. Run Shipping Agent Demo (Human-in-the-loop)")
        print("3. Exit")
        
        choice: str = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            await run_image_demo()
        elif choice == "2":
            await run_shipping_demos()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main())
