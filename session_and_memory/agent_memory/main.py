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

