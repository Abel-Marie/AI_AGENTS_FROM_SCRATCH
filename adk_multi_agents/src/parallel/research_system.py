from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from src.config import get_retry_config

def create_research_system():
    retry_config = get_retry_config()

