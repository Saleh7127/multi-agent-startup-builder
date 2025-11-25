import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from memory.memory_tools import get_latest_tool

load_dotenv()

ROUTER_PROMPT = """
You are an intelligent router. Answer questions about previous agent responses by querying the database.

If the user asks about a previous agent response (e.g., "what was the last response from idea_intake_agent"), use get_latest_agent_response tool with the agent_name and return the response_json.

Agent name format: "agent_name_agent" (e.g., "idea_intake_agent", "financial_projections_agent")

If the input is NOT a query about previous responses (it's a new startup idea), return exactly: "ROUTE_TO_PIPELINE"
"""

intelligent_router_agent = LlmAgent(
    name="intelligent_router_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=ROUTER_PROMPT,
    tools=[get_latest_tool],
    output_key="router_result",
)

