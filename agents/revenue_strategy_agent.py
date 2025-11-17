import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.revenue_strategy_prompt import REVENUE_STRATEGY_PROMPT

load_dotenv()

revenue_strategy_agent = Agent(
    name="revenue_strategy_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=REVENUE_STRATEGY_PROMPT,
    output_key="revenue_strategy_result",
)

