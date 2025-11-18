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
from prompts.market_analysis_prompt import MARKET_ANALYSIS_PROMPT
from agents.google_search_agent import google_search_agent
from agents.idea_intake_agent import idea_intake_agent

load_dotenv()

# Create AgentTool wrapper for the google_search_agent
search_tool = AgentTool(agent=google_search_agent)
idea_intake_tool = AgentTool(agent=idea_intake_agent)

market_analysis_agent = Agent(
    name="market_analysis_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=MARKET_ANALYSIS_PROMPT,
    tools=[google_search],
    output_key="market_analysis_result",
)

