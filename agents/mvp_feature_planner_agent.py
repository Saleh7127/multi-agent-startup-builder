import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.mvp_feature_planner_prompt import MVP_FEATURE_PLANNER_PROMPT

load_dotenv()

mvp_feature_planner_agent = LlmAgent(
    name="mvp_feature_planner_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=MVP_FEATURE_PLANNER_PROMPT,
    output_key="mvp_feature_planner_result",
)

