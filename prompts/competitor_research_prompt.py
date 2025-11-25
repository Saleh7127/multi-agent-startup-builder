COMPETITOR_RESEARCH_PROMPT = """
Analyze {idea_intake_result}. Use google_search. Keep concise. Return JSON only:

{
  "direct_competitors": [{"name": "Name", "description": "Brief", "business_model": "Model", "strengths": ["S1"], "weaknesses": ["W1"]}],
  "indirect_competitors": [{"name": "Name", "why_indirect": "Reason"}],
  "competitive_landscape": "Brief summary",
  "market_gaps": ["Gap1", "Gap2"],
  "differentiation_opportunities": ["Opp1", "Opp2"]
}
"""