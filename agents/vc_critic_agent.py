"""VC Critic Agent - Evaluates pitch decks and provides feedback for iterative refinement."""

import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.vc_critic_prompt import VC_CRITIC_PROMPT

load_dotenv()

vc_critic_agent = LlmAgent(
    name="vc_critic_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=VC_CRITIC_PROMPT,
    output_key="vc_critic_result",
)

