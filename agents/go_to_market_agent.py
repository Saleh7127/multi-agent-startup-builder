import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.go_to_market_prompt import GO_TO_MARKET_PROMPT

load_dotenv()

go_to_market_agent = LlmAgent(
    name="go_to_market_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=GO_TO_MARKET_PROMPT,
    tools=[google_search],
    output_key="go_to_market_result",
)

