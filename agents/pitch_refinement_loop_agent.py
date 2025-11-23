"""Pitch Refinement Loop Agent - Iteratively refines pitch deck based on VC Critic feedback (max 3 iterations)."""

import sys
from pathlib import Path
from google.adk.agents import LoopAgent

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .pitch_deck_agent import pitch_deck_agent
from .vc_critic_agent import vc_critic_agent

# LoopAgent iterates through sub_agents in sequence, repeating until max_iterations reached
# In each iteration:
# 1. Pitch Deck Agent creates/updates pitch deck (can access vc_critic_result from previous iteration)
# 2. VC Critic Agent evaluates the pitch deck
# If VC Critic approves (status == "approved"), the loop should exit early (handled by LoopAgent logic)
# Otherwise, loop continues up to max_iterations=3
pitch_refinement_loop_agent = LoopAgent(
    name="pitch_refinement_loop_agent",
    description="Iteratively refines pitch deck based on VC Critic feedback. Loops until approved or max 3 iterations",
    sub_agents=[
        pitch_deck_agent,  # Creates/updates pitch deck (uses vc_critic_result from previous iteration if available)
        vc_critic_agent,   # Evaluates pitch deck and provides feedback
    ],
    max_iterations=3,
)

