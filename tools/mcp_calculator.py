"""
MCP Calculator Tool - Wrapped with error handling to prevent async context issues.
"""

from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Create MCP calculator with increased timeout and proper error handling
try:
    mcp_calculator = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="python",
                args=["-m", "mcp_server_calculator"],
            ),
            timeout=60,  # Increased timeout to prevent premature cleanup
        )
    )
except Exception as e:
    # If MCP calculator fails to initialize, create a None placeholder
    # The agent can still work without it, just won't have calculator functionality
    print(f"Warning: MCP calculator initialization failed: {e}")
    mcp_calculator = None

