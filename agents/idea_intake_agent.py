
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.idea_intake_prompt import IDEA_INTAKE_PROMPT

load_dotenv()

idea_intake_agent = Agent(
    name="idea_intake_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=IDEA_INTAKE_PROMPT,
    output_key="idea_intake_result",
)

async def main():
    """Run the idea intake agent with a test idea."""
    runner = InMemoryRunner(agent=idea_intake_agent)
    response = await runner.run_debug(
        "An AI that helps students revise and improve assignments"
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())