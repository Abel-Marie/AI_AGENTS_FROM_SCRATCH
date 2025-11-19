from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from src.config import get_retry_config

def create_research_system():
    retry_config = get_retry_config()

    # Tech Researcher
    tech_researcher = Agent(
        name="TechResearcher",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Research the latest AI/ML trends. Include 3 key developments,
    the main companies involved, and the potential impact. Keep the report very concise (100 words).""",
        tools=[google_search],
        output_key="tech_research",
    )