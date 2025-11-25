PITCH_DECK_PROMPT = """
Synthesize {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}, {financial_projections_result}, {go_to_market_result}, {visual_identity_result} into pitch deck.

If revision iteration, check context for vc_critic_result and incorporate feedback. Keep sections concise. Return JSON only:

{
  "company_name": "Name",
  "tagline": "Brief",
  "logo_path": "Path or TODO",
  "elevator_pitch": "1-2 sentences",
  "sections": [{"title": "Title", "bullets": ["B1", "B2", "B3"]}],
  "metrics_snapshot": {
    "market": ["TAM/SAM"],
    "product": ["MVP"],
    "business_model": ["Pricing"],
    "go_to_market": ["Channels"],
    "finance": ["Revenue"]
  },
  "investment_ask": {
    "amount": "Amount",
    "use_of_funds": ["U1", "U2", "U3"],
    "milestones": ["M1", "M2"],
    "timeline": "Brief"
  },
  "call_to_action": "Brief CTA",
  "risks": ["R1", "R2"],
  "appendix": ["N1"]
}
"""

