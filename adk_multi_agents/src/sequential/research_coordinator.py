from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, google_search
from src.config import get_retry_config 

def create_research_coordinator():
    retry_config = get_retry_config()

    