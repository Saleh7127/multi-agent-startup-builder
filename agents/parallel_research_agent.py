"""Parallel Research Agent - Runs Market Analysis and Competitor Research in parallel."""

import sys
from pathlib import Path
from google.adk.agents import ParallelAgent

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from .market_analysis_agent import market_analysis_agent
from .competitor_research_agent import competitor_research_agent

parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    description="Runs Market Analysis and Competitor Research agents in parallel for efficiency",
    sub_agents=[
        market_analysis_agent,
        competitor_research_agent,
    ],
)

