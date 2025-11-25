MARKET_ANALYSIS_PROMPT = """
Analyze {idea_intake_result}. Use google_search. Keep concise. Return JSON only:

{
  "market_size": "TAM/SAM",
  "market_trends": ["Trend1", "Trend2"],
  "market_opportunities": ["Opp1", "Opp2"],
  "market_challenges": ["Challenge1"],
  "target_segments": ["Segment1", "Segment2"],
  "growth_potential": "Brief assessment",
  "market_maturity": "emerging|growing|mature|declining"
}
"""