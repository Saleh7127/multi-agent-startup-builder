import asyncio
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config
from prompts.pitch_deck_prompt import PITCH_DECK_PROMPT
from tools.pdf_generation_tool import pdf_generation_tool


load_dotenv()

# Enhanced instruction that includes access to all previous agent outputs and PDF generation
PITCH_DECK_WITH_PDF_INSTRUCTION = """
Synthesize {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}, {financial_projections_result}, {go_to_market_result}, {visual_identity_result} into pitch deck.

Return JSON only, then call pdf_generation_tool:

{
  "company_name": "Name",
  "tagline": "Tagline",
  "logo_path": "Path or TODO",
  "elevator_pitch": "2-3 sentences",
  "sections": [{"title": "Title", "bullets": ["Bullet1"]}],
  "metrics_snapshot": {
    "market": ["TAM/SAM"],
    "product": ["MVP status"],
    "business_model": ["Pricing"],
    "go_to_market": ["Channels"],
    "finance": ["Revenue"]
  },
  "investment_ask": {
    "amount": "Amount",
    "use_of_funds": ["Use1"],
    "milestones": ["Milestone1"],
    "timeline": "Timeline"
  },
  "call_to_action": "CTA",
  "risks_or_diligence": ["Risk1"],
  "appendix_notes": ["Note1"]
}
"""

pitch_deck_agent = LlmAgent(
    name="pitch_deck_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=retry_config
    ),
    instruction=PITCH_DECK_WITH_PDF_INSTRUCTION,
    tools=[pdf_generation_tool],
    output_key="pitch_deck_result",
)


async def main():
    """Quick smoke test for the pitch deck agent."""
    runner = InMemoryRunner(agent=pitch_deck_agent)
    sample_payload = {
        "startup_idea": "AI platform that predicts crop yield for regenerative farms.",
        "agent_results": {
            "market_analysis_result": {
                "market_size": "TAM $12B",
                "market_trends": ["Sustainable ag premium"],
            },
            "visual_identity_result": {
                "logo_assets": {
                    "generated_files": ["generated_assets/logos/sample_logo.png"]
                }
            }
        }
    }
    response = await runner.run_debug(
        json.dumps(sample_payload, indent=2),
        quiet=True
    )
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
