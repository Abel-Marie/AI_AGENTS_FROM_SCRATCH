from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, google_search
from src.config import get_retry_config 

def create_research_coordinator():
    retry_config = get_retry_config()

    # Research Agent
    research_agent = Agent(
        name="ResearchAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized research agent. Your only job is to use the 
        google_search tool to find 2-3 pieces of relevant information on the given topic and present the finidings with citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

