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