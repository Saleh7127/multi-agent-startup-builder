"""Pitch Deck Agent - Creates pitch deck from all agent outputs, incorporating VC feedback if available."""

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


def add_vc_feedback_callback(context):
    """Callback to dynamically add VC feedback to instruction if available in state."""
    # Get current instruction
    instruction = PITCH_DECK_PROMPT
    
    # Check if vc_critic_result exists in state
    state = getattr(context, 'state', None)
    if state and hasattr(state, 'get'):
        vc_feedback = state.get("vc_critic_result")
        if vc_feedback:
            # Add VC feedback section before "Return JSON only:"
            vc_section = f"""

IMPORTANT - REVISION ITERATION: The following VC feedback was provided on a previous version. Please incorporate this feedback to improve the pitch deck:

{vc_feedback}

Instructions:
- Address all critical issues mentioned above
- Incorporate all feedback suggestions
- Maintain strengths while addressing weaknesses
- Improve the overall quality and investor appeal

"""
            instruction = instruction.replace("Return JSON only:", vc_section + "Return JSON only:")
    
    return instruction


pitch_deck_agent = LlmAgent(
    name="pitch_deck_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=PITCH_DECK_PROMPT,
    output_key="pitch_deck_result",
)
