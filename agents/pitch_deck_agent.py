import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.pitch_deck_prompt import PITCH_DECK_PROMPT

load_dotenv()

pitch_deck_agent = LlmAgent(
    name="pitch_deck_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=PITCH_DECK_PROMPT,
    output_key="pitch_deck_result",
)
