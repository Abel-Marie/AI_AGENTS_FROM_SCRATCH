from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from .config import get_retry_config
from .tools import set_device_status

def create_home_automation_agent():
    """Creates a home automation agent with deliberate flaws for evaluation.
    
    This agent has intentional issues:
    - Overly broad claims about capabilities
    - May hallucinate device features
    - Inconsistent response formatting
    """
    retry_config = get_retry_config()
    
    return LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="home_automation_agent",
        description="An agent to control smart devices in a home.",
        instruction="""You are a home automation assistant. You control ALL smart devices in the house.
        
        You have access to lights, security systems, ovens, fireplaces, and any other device the user mentions.
        Always try to be helpful and control whatever device the user asks for.
        
        When users ask about device capabilities, tell them about all the amazing features you can control.""",
        tools=[set_device_status],
    )
