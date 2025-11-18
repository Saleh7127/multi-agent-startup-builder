import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, google_search

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.go_to_market_prompt import GO_TO_MARKET_PROMPT
from agents.google_search_agent import google_search_agent

load_dotenv()

# Create AgentTool wrapper for the google_search_agent
search_tool = AgentTool(agent=google_search_agent)

go_to_market_agent = Agent(
    name="go_to_market_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=GO_TO_MARKET_PROMPT,
    tools=[google_search],
    output_key="go_to_market_result",
)

