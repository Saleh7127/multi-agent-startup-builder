PITCH_DECK_PROMPT = """
Synthesize {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}, {financial_projections_result}, {go_to_market_result}, {visual_identity_result} into pitch deck.

Note: If this is a revision iteration and VC feedback is available from a previous iteration, review the conversation history for vc_critic_result and incorporate the feedback to improve the pitch deck.

Return JSON only:

{
  "company_name": "Name",
  "tagline": "Tagline",
  "logo_path": "Path from visual_identity_result or TODO",
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

