from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from src.config import get_retry_config

def create_blog_pipeline():
    retry_config = get_retry_config()

    # Outline Agent
    outline_agent = Agent(
        name="OutlineAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Create a blog outline for the given topic with:
        1. A catchy headline
        2. An introduction hook
        3. 3-5 main sections with 2-3 bullet points for each
        4. A concluding thought""",
        output_key="blog_outline",
    )

    # Writer Agent
    writer_agent = Agent(
        name="WriterAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Following this outline strictly: {blog_outline}
        Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
        output_key="blog_draft",
    )

    # Editor Agent
    editor_agent = Agent(
        name="EditorAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""Edit this draft: {blog_draft}
        Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
        output_key="final_blog",
    )

    # Sequential Root Agent
    root_agent = SequentialAgent(
        name="BlogPipeline",
        sub_agents=[outline_agent, writer_agent, editor_agent],
    )
    
    return root_agent
