from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from typing import List
from .config import get_retry_config

def count_papers(papers: List[str]):
    """
    This function counts the number of papers in a list of strings.
    Args:
      papers: A list of strings, where each string is a research paper.
    Returns:
      The number of papers in the list.
    """
    return len(papers)

def create_fixed_agent():
    """Creates the agent with the correct type hint."""
    retry_config = get_retry_config()
    
    # Google Search agent
    google_search_agent = LlmAgent(
        name="google_search_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        description="Searches for information using Google search",
        instruction="""Use the google_search tool to find information on the given topic. Return the raw search results.
        If the user asks for a list of papers, then give them the list of research papers you found and not the summary.""",
        tools=[google_search]
    )

    # Root agent
    return LlmAgent(
        name="research_paper_finder_agent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Your task is to find research papers and count them. 
   
       You must follow these steps:
       1) Find research papers on the user provided topic using the 'google_search_agent'. 
       2) Then, pass the papers to 'count_papers' tool to count the number of papers returned.
       3) Return both the list of research papers and the total number of papers.
       """,
        tools=[AgentTool(agent=google_search_agent), count_papers]
    )
