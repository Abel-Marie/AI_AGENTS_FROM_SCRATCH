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

def create_llm_agent(name="text_chat_bot", description="A text chatbot"):
    """Creates an LlmAgent (needed for DatabaseSessionService)."""
    retry_config = get_retry_config()
    return LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name=name,
        description=description,
    )
def create_stateful_agent():
    """Creates an agent with session state tools."""
    retry_config = get_retry_config()
    return LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="""A text chatbot.
        Tools for managing user context:
        * To record username and country when provided use `save_userinfo` tool. 
        * To fetch username and country when required use `retrieve_userinfo` tool.
        """,
        tools=[save_userinfo, retrieve_userinfo],
    )

def create_app_with_compaction(agent):
    """Creates an App with events compaction enabled."""
    return App(
        name="research_app_compacting",
        root_agent=agent,
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # Trigger compaction every 3 invocations
            overlap_size=1,  # Keep 1 previous turn for context
        ),
    )

