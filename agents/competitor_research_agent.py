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
from prompts.competitor_research_prompt import COMPETITOR_RESEARCH_PROMPT


load_dotenv()

competitor_research_agent = Agent(
    name="competitor_research_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=COMPETITOR_RESEARCH_PROMPT,
    tools=[google_search],
    output_key="competitor_research_result",
)

