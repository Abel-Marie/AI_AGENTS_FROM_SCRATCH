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
