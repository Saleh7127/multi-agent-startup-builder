"""PDF Generation Agent - Generates PDF from pitch deck JSON."""

import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.pdf_generation_prompt import PDF_GENERATION_PROMPT
from tools.pdf_generation_tool import pdf_generation_tool

load_dotenv()

pdf_generation_agent = LlmAgent(
    name="pdf_generation_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=PDF_GENERATION_PROMPT,
    tools=[pdf_generation_tool],
    output_key="pdf_generation_result",
)

