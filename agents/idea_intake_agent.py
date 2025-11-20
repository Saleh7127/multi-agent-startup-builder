
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
from prompts.idea_intake_prompt import IDEA_INTAKE_PROMPT

load_dotenv()

idea_intake_agent = LlmAgent(
    name="idea_intake_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=IDEA_INTAKE_PROMPT,
    output_key="idea_intake_result",
)
