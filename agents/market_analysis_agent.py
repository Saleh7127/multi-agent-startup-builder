import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.market_analysis_prompt import MARKET_ANALYSIS_PROMPT


load_dotenv()

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

