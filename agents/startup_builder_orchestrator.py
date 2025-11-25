"""
Startup Builder Orchestrator - Orchestrates all agents using Google ADK with parallel processing and iterative refinement.
This agent chains agents together with parallel execution where possible and iterative loops for refinement.

New Architecture:
1. Idea Intake (Sequential)
2. Market Analysis + Competitor Research (PARALLEL)
3. Customer Persona (Sequential - synthesizes research)
4. MVP Planner + Tech Architect + Revenue Strategy (PARALLEL)
5. Financial → GTM → Visual Identity (Sequential)
6. Pitch Deck ↔ VC Critic (LOOP - max 3 iterations)
7. PDF Generation (Sequential - only if approved)

For detailed workflow documentation, see prompts.root_agent_prompt.ROOT_AGENT_WORKFLOW
"""

import sys
from pathlib import Path
from google.adk.agents import SequentialAgent
from google.adk.runners import InMemoryRunner


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import root agent workflow documentation
from prompts.orchestrator_agent_prompt import ORCHESTRATOR_PROMPT

# Import individual agents
from .idea_intake_agent import idea_intake_agent
from .customer_persona_agent import customer_persona_agent
from .financial_projections_agent import financial_projections_agent
from .go_to_market_agent import go_to_market_agent
from .visual_identity_agent import visual_identity_agent
from .pdf_generation_agent import pdf_generation_agent

# Import parallel and loop agents
from .parallel_research_agent import parallel_research_agent
from .parallel_planning_agent import parallel_planning_agent
from .pitch_refinement_loop_agent import pitch_refinement_loop_agent
from memory.auto_storage_callback import auto_store_agent_responses

# Create the improved SequentialAgent that orchestrates phases:
# Each phase can be a sequential, parallel, or loop agent
startup_builder_orchestrator = SequentialAgent(
    name="StartupBuilderOrchestrator",
    description=ORCHESTRATOR_PROMPT,
    after_agent_callback=auto_store_agent_responses,
    sub_agents=[
        # Phase 1: Idea Intake (Sequential)
        idea_intake_agent,
        
        # Phase 2: Parallel Research (ParallelAgent)
        parallel_research_agent,
        
        # Phase 3: Customer Persona (Sequential - synthesizes research)
        customer_persona_agent,
        
        # Phase 4: Parallel Planning (ParallelAgent)
        parallel_planning_agent,
        
        # Phase 5: Sequential Execution (SequentialAgent)
        # Financial depends on revenue_strategy (from parallel planning)
        financial_projections_agent,
        # GTM can run after customer_persona is ready
        go_to_market_agent,
        # Visual Identity can run independently
        visual_identity_agent,
        
        # Phase 6: Iterative Pitch Refinement (LoopAgent)
        pitch_refinement_loop_agent,
        
        # Phase 7: PDF Generation (Sequential - only runs after loop exits)
        pdf_generation_agent,
    ],
)

# Recursively attach the callback to all sub-agents to ensure intermediate results are stored
def attach_callback_recursive(agent):
    if hasattr(agent, 'after_agent_callback') and agent.after_agent_callback is None:
        agent.after_agent_callback = auto_store_agent_responses
    
    if hasattr(agent, 'sub_agents') and agent.sub_agents:
        for sub in agent.sub_agents:
            attach_callback_recursive(sub)

attach_callback_recursive(startup_builder_orchestrator)

# Export both the class and instance
StartupBuilderOrchestrator = startup_builder_orchestrator

runner = InMemoryRunner(agent=startup_builder_orchestrator)

# Export the workflow documentation for reference
__all__ = ["startup_builder_orchestrator", "StartupBuilderOrchestrator", "ORCHESTRATOR_PROMPT"]

