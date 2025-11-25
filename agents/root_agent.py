import sys
from pathlib import Path
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from .memory_router_agent import memory_router_agent
from .startup_builder_orchestrator import startup_builder_orchestrator

load_dotenv()

ROOT_AGENT_PROMPT = """
You are the Root Agent that routes user requests intelligently.

Your workflow:
1. FIRST: Call memory_router_agent tool with the user's query to check if it can be answered from memory
2. If memory_router_agent returns an answer from memory → Return that answer to the user
3. If memory_router_agent doesn't have the answer:
   - If it's a STARTUP IDEA (keywords: build, create, develop, startup, business idea, company, product, service) → Call startup_builder_orchestrator tool with the user's startup idea
   - If it's NOT a startup idea → Respond: "I don't have that knowledge. I can only help with startup building tasks."

Important: Always call memory_router_agent first to check memory. Only call startup_builder_orchestrator if memory doesn't have the answer AND it's a startup idea.
"""

root_agent = LlmAgent(
    name="RootAgent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=ROOT_AGENT_PROMPT,
    tools=[AgentTool(agent=memory_router_agent), AgentTool(agent=startup_builder_orchestrator)],
)
