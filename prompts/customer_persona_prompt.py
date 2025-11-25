CUSTOMER_PERSONA_PROMPT = """
Create 2 personas from {idea_intake_result}, {market_analysis_result}, {competitor_research_result}. Keep concise. Return JSON only:

{
  "personas": [{
    "name": "Name",
    "age_range": "Range",
    "occupation": "Role",
    "demographics": {"location": "Loc", "income": "Income", "education": "Edu"},
    "psychographics": {"values": ["V1", "V2"], "interests": ["I1"]},
    "behaviors": {"online": "Brief", "purchasing": "Brief"},
    "pain_points": ["Pain1", "Pain2"],
    "goals": ["Goal1", "Goal2"],
    "needs": ["Need1", "Need2"],
    "channels": ["Channel1"]
  }],
  "persona_summary": "1-2 sentences"
}
"""

