"""Parallel Planning Agent - Runs MVP Feature Planner, Technical Architect, and Revenue Strategy in parallel."""

import sys
from pathlib import Path
from google.adk.agents import ParallelAgent

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .mvp_feature_planner_agent import mvp_feature_planner_agent
from .technical_architect_agent import technical_architect_agent
from .revenue_strategy_agent import revenue_strategy_agent

parallel_planning_agent = ParallelAgent(
    name="parallel_planning_agent",
    description="Runs MVP Feature Planner, Technical Architect, and Revenue Strategy agents in parallel",
    sub_agents=[
        mvp_feature_planner_agent,
        technical_architect_agent,
        revenue_strategy_agent,
    ],
)

