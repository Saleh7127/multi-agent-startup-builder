import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.technical_architect_prompt import TECHNICAL_ARCHITECT_PROMPT

load_dotenv()

technical_architect_agent = LlmAgent(
    name="technical_architect_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=TECHNICAL_ARCHITECT_PROMPT,
    output_key="technical_architect_result",
)

