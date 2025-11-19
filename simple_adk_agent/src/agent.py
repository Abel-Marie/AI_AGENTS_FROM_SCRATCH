from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search 
from .config import get_retry_config 


def create_agent():
    retry_config = get_retry_config()

    return Agent(
        name = "helpful_assistant",
        model = Gemini(
            model = "gemini-2.5-flash-lite",
            retry_options=retry_config
        ),
        description="a simple agent that can answer general questions.",
        instruction="You are a helpful assistant. Use Google Search For current info or if unsure.",
        tools=[google_search],
    )
