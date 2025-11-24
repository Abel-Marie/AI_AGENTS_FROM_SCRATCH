from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import load_memory, preload_memory
from google.genai import types
from .callbacks import auto_save_to_memory
from .config import get_retry_config

def create_memory_agent(name="MemoryDemoAgent"):
    """Creates a basic agent."""
    retry_config = get_retry_config()
    return LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name=name,
        instruction="Answer user questions in simple words.",
    )

def create_agent_with_load_memory(name="MemoryDemoAgent"):
    """Creates an agent with load_memory tool."""
    retry_config = get_retry_config()
    return LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name=name,
        instruction="Answer user questions in simple words. Use load_memory tool if you need to recall past conversations.",
        tools=[load_memory],
    )


def create_auto_memory_agent(name="AutoMemoryAgent"):
    """Creates an agent with auto-save callback and preload_memory."""
    retry_config = get_retry_config()
    return LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name=name,
        instruction="Answer user questions.",
        tools=[preload_memory],
        after_agent_callback=auto_save_to_memory,
    )
