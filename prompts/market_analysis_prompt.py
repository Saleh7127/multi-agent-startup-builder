MARKET_ANALYSIS_PROMPT = """
Analyze {idea_intake_result} and use google_search tools for market research. Return JSON only:

{
  "market_size": "TAM/SAM estimate",
  "market_trends": ["Trend 1", "Trend 2"],
  "market_opportunities": ["Opportunity 1"],
  "market_challenges": ["Challenge 1"],
  "target_segments": ["Segment 1"],
  "growth_potential": "Growth assessment",
  "market_maturity": "emerging|growing|mature|declining"
}
"""