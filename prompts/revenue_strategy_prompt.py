REVENUE_STRATEGY_PROMPT = """
Analyze {idea_intake_result}, {market_analysis_result}, {customer_persona_result}. Return JSON only:

{
  "revenue_models": [{"model_name": "Name", "description": "Desc", "applicability": "Why", "pros": ["Pro1"], "cons": ["Con1"], "recommended": true}],
  "pricing_strategy": {
    "primary_model": "Model",
    "pricing_tiers": [{"tier_name": "Tier", "price": "Price", "features": ["F1"], "target_segment": "Segment"}],
    "pricing_rationale": "Rationale",
    "competitive_positioning": "Positioning"
  },
  "revenue_strategy_considerations": {
    "market_factors": ["Factor1"],
    "customer_willingness": "Willingness",
    "scalability": "Scalability",
    "risks": ["Risk1"]
  }
}
"""

