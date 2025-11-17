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
from prompts.financial_projections_prompt import FINANCIAL_PROJECTIONS_PROMPT
from tools.mcp_calculator import mcp_calculator

load_dotenv()

financial_projections_agent = Agent(
    name="financial_projections_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=FINANCIAL_PROJECTIONS_PROMPT,
    tools=[mcp_calculator],
    output_key="financial_projections_result",
)

