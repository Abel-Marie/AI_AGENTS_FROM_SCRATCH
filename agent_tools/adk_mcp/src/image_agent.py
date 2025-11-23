import os
import base64
from IPython.display import display, Image as IPImage
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from .config import get_retry_config


def create_image_agent():
    """Creates an agent with MCP integration for image generation."""
    retry_config = get_retry_config()
    
    # MCP integration with Everything Server
    mcp_image_server = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",  # Run MCP server via npx
                args=[
                    "-y",  # Argument for npx to auto-confirm install
                    "@modelcontextprotocol/server-everything",
                ],
                tool_filter=["getTinyImage"],
            ),
            timeout=30,
        )
    )

    # Create image agent with MCP integration
    image_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="image_agent",
        instruction="Use the MCP Tool to generate images for user queries",
        tools=[mcp_image_server],
    )
    
    return image_agent

async def run_image_demo():
    """Runs the image generation demo."""
    print("--- Running MCP Image Agent Demo ---")
    agent = create_image_agent()
    runner = InMemoryRunner(agent=agent)
    
    query = "Provide a sample tiny image"
    print(f"Running query: {query}")
    
    response = await runner.run_debug(query, verbose=True)
    
    # Save and display the image
    # Get the directory of the current file (src/image_agent.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to adk_mcp/ and then into generated_images/
    output_dir = os.path.join(os.path.dirname(current_dir), "generated_images")
    os.makedirs(output_dir, exist_ok=True)
    
    for event in response:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "function_response") and part.function_response:
                    for item in part.function_response.response.get("content", []):
                        if item.get("type") == "image":
                            image_data = base64.b64decode(item["data"])
                            file_path = os.path.join(output_dir, "tiny_image.png")
                            with open(file_path, "wb") as f:
                                f.write(image_data)
                            print(f"✅ Image saved to: {file_path}")
