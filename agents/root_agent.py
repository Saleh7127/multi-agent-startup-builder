"""
ROOT Agent - Orchestrates all agents sequentially using Google ADK SequentialAgent.
This agent chains all individual agents together, passing outputs from one to the next.

For detailed workflow documentation, see prompts.root_agent_prompt.ROOT_AGENT_WORKFLOW
"""

import sys
from pathlib import Path
from google.adk.agents import SequentialAgent
from google.adk.runners import InMemoryRunner


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import root agent workflow documentation
from prompts.root_agent_prompt import ROOT_AGENT_WORKFLOW

# Import all individual agents
from .idea_intake_agent import idea_intake_agent
from .market_analysis_agent import market_analysis_agent
from .competitor_research_agent import competitor_research_agent
from .customer_persona_agent import customer_persona_agent
from .mvp_feature_planner_agent import mvp_feature_planner_agent
from .technical_architect_agent import technical_architect_agent
from .revenue_strategy_agent import revenue_strategy_agent
from .financial_projections_agent import financial_projections_agent
from .go_to_market_agent import go_to_market_agent
from .visual_identity_agent import visual_identity_agent
from .pitch_deck_agent import pitch_deck_agent

# Create the SequentialAgent that chains all agents together
# Each agent can access previous agent outputs using {output_key} placeholders
# 
# Workflow Documentation:
# The root agent orchestrates 11 specialized agents in sequence:
# 1. Idea Intake → 2. Market Analysis → 3. Competitor Research → 4. Customer Persona →
# 5. MVP Feature Planner → 6. Technical Architect → 7. Revenue Strategy →
# 8. Financial Projections → 9. Go-to-Market → 10. Visual Identity → 11. Pitch Deck
#
# The ROOT_AGENT_WORKFLOW provides complete workflow details, agent duties, inputs, and outputs
root_agent = SequentialAgent(
    name="RootAgent",
    description=ROOT_AGENT_WORKFLOW,  # Use workflow documentation as description
    sub_agents=[
        idea_intake_agent,
        market_analysis_agent,
        competitor_research_agent,
        customer_persona_agent,
        mvp_feature_planner_agent,
        technical_architect_agent,
        revenue_strategy_agent,
        financial_projections_agent,
        go_to_market_agent,
        visual_identity_agent,
        pitch_deck_agent,
    ],
)

# Export both the class and instance
RootAgent = root_agent

runner = InMemoryRunner(agent=root_agent)

# Export the workflow documentation for reference
__all__ = ["root_agent", "RootAgent", "ROOT_AGENT_WORKFLOW"]

