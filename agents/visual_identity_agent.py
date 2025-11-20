import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.visual_identity_prompt import VISUAL_IDENTITY_PROMPT
from tools.logo_generation_tool import logo_generation_tool


load_dotenv()

visual_identity_agent = LlmAgent(
    name="visual_identity_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=VISUAL_IDENTITY_PROMPT,
    tools=[logo_generation_tool],
    output_key="visual_identity_result",
)

