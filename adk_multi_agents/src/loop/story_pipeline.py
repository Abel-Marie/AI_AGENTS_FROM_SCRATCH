from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from src.config import get_retry_config

def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

def create_story_pipeline():
    retry_config = get_retry_config()

    # Initial Writer Agent
    initial_writer_agent = Agent(
        name="InitialWriterAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
        Output only the story text, with no introduction or explanation.""",
        output_key="current_story",
    )

    # Critic Agent
    critic_agent = Agent(
        name="CriticAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a constructive story critic. Review the story provided below.
        Story: {current_story}
        
        Evaluate the story's plot, characters, and pacing.
        - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
        - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
        output_key="critique",
    )

