REVENUE_STRATEGY_PROMPT = """
Analyze {idea_intake_result}, {market_analysis_result}, {customer_persona_result}. Keep concise. Return JSON only:

{
  "revenue_models": [{"model_name": "Name", "description": "Brief", "applicability": "Brief", "pros": ["P1"], "cons": ["C1"], "recommended": true}],
  "pricing_strategy": {
    "primary_model": "Model",
    "pricing_tiers": [{"tier_name": "Tier", "price": "Price", "features": ["F1", "F2"], "target_segment": "Segment"}],
    "pricing_rationale": "Brief",
    "competitive_positioning": "Brief"
  },
  "considerations": {
    "market_factors": ["F1", "F2"],
    "customer_willingness": "Brief",
    "scalability": "Brief",
    "risks": ["R1"]
  }
}
"""

