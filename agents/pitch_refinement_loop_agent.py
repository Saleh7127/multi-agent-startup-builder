import sys
from pathlib import Path
from google.adk.agents import LoopAgent

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .pitch_deck_agent import pitch_deck_agent
from .vc_critic_agent import vc_critic_agent

pitch_refinement_loop_agent = LoopAgent(
    name="pitch_refinement_loop_agent",
    description="Iteratively refines pitch deck based on VC Critic feedback. Loops up to 3 iterations",
    sub_agents=[
        pitch_deck_agent,
        vc_critic_agent,
    ],
    max_iterations=3,
)

