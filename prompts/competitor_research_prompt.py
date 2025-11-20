COMPETITOR_RESEARCH_PROMPT = """
Analyze {idea_intake_result} and use google_search to find competitors. Return JSON only:

{
  "direct_competitors": [{"name": "Name", "description": "Desc", "business_model": "Model", "strengths": ["S1"], "weaknesses": ["W1"], "market_position": "Position"}],
  "indirect_competitors": [{"name": "Name", "description": "Desc", "why_indirect": "Reason"}],
  "competitive_landscape": "Landscape summary",
  "market_gaps": ["Gap 1"],
  "differentiation_opportunities": ["Opp 1"]
}
"""