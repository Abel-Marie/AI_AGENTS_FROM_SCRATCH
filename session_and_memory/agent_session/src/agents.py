from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from .config import get_retry_config
from .tools import save_userinfo, retrieve_userinfo


def create_text_agent(name="text_chat_bot", description="A text chatbot"):
    """Creates a basic text chatbot agent."""
    retry_config = get_retry_config()
    return Agent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name=name,
        description=description,
    )
