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

    # Refiner Agent
    refiner_agent = Agent(
        name="RefinerAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a story refiner. You have a story draft and critique.
        
        Story Draft: {current_story}
        Critique: {critique}
        
        Your task is to analyze the critique.
        - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
        - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
        output_key="current_story",
        tools=[FunctionTool(exit_loop)],
    )

    