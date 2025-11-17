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
from prompts.customer_persona_prompt import CUSTOMER_PERSONA_PROMPT

load_dotenv()

customer_persona_agent = Agent(
    name="customer_persona_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=CUSTOMER_PERSONA_PROMPT,
    output_key="customer_persona_result",
)

