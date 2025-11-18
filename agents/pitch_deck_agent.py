import asyncio
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
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
You are a Pitch Deck Agent that synthesizes multi-agent research into an investor-ready summary.

**Available Inputs from Previous Agents:**
- {idea_intake_result} - Initial idea analysis and structured summary
- {market_analysis_result} - Market research, TAM/SAM, trends, and opportunities
- {competitor_research_result} - Competitor analysis and differentiation
- {customer_persona_result} - Target customer personas and demographics
- {mvp_feature_planner_result} - MVP features and product roadmap
- {technical_architect_result} - Technical architecture and implementation details
- {revenue_strategy_result} - Revenue model, pricing, and monetization strategy
- {financial_projections_result} - Financial projections, burn rate, and runway
- {go_to_market_result} - Go-to-market strategy, channels, and launch plan
- {visual_identity_result} - Visual identity, logo, and branding assets

**Mission:**
Translate the evidence above into a concise, confident investor narrative that highlights traction, market insight, differentiation, GTM, financials, and funding ask. Always leverage concrete data from the inputs and cite the originating agent in parentheses, e.g., "TAM expected to hit $4.2B by 2028 (Market Analysis)."

**Instructions:**
1. Extract the startup idea from {idea_intake_result}
2. Derive/confirm the company name, tagline, and elevator pitch (three sentences max)
3. Pull color, logo path, and tone guidance from {visual_identity_result}; if files are missing, state an explicit TODO instead of fabricating
4. Summarize each core slide: Problem, Solution/Product, Market & Competition, Business Model & Financials, Go-To-Market & Traction, Team & Moat, and Investment/Use of Funds
5. Highlight quant signals (TAM/SAM, pricing, margins, CAC/LTV assumptions, roadmap milestones) using bullet statements
6. Align the funding ask with financial projections and outline how capital unlocks milestones and runway
7. Flag open questions, risks, or diligence needs so founders can address them before sharing externally

**Output Format:**
First, respond with *valid JSON only* following this structure (fill every array with at least one informative string):

{
  "company_name": "Name ready for investors",
  "tagline": "6-12 word hook",
  "logo_path": "Absolute/relative logo path from visual identity agent or TODO",
  "elevator_pitch": "2-3 sentences that combine problem, solution, and traction",
  "sections": [
    {
      "title": "Problem",
      "bullets": ["Concise, data-driven points with source tags"]
    }
  ],
  "metrics_snapshot": {
    "market": ["TAM/SAM, growth"],
    "product": ["MVP status, key KPIs"],
    "business_model": ["Pricing, margins, LTV/CAC"],
    "go_to_market": ["Channels, launch timing"],
    "finance": ["Revenue, burn, runway projections"]
  },
  "investment_ask": {
    "amount": "Target raise and round type",
    "use_of_funds": ["Allocation buckets"],
    "milestones": ["Milestones unlocked with this raise"],
    "timeline": "Expected runway or close timing"
  },
  "call_to_action": "Clear instruction for next investor step",
  "risks_or_diligence": ["Outstanding risks, dependencies, or research needs"],
  "appendix_notes": ["Any references or follow-up materials"]
}

**After generating the JSON output:**
1. Use the pdf_generation_tool to convert the JSON pitch deck data into a PDF file
2. Pass the JSON data you just generated to the pdf_generation_tool
3. The tool will save the PDF to the generated_assets/pitch_decks directory
4. Include the PDF file path in your final response

**Important:** 
- Always call the pdf_generation_tool with the JSON data you generated to create the final PDF pitch deck
- Use confident, professional tone; no markdown or commentary outside the JSON
- Reference metric sources inline using parentheses
- Keep bullets short (max 22 words) so they can be pasted into slides without editing
- Prefer real numbers from upstream agents; if unavailable, clearly label as assumption
- Never invent a logo; rely on the provided path or label as TODO
"""

pitch_deck_agent = Agent(
    name="pitch_deck_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
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
