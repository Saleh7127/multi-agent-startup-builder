CUSTOMER_PERSONA_PROMPT = """
Create 3-5 personas from {idea_intake_result} and {market_analysis_result}. Return JSON only:

{
  "personas": [{
    "name": "Name",
    "age_range": "Range",
    "occupation": "Role",
    "demographics": {"location": "Loc", "income_level": "Income", "education": "Edu", "family_status": "Status"},
    "psychographics": {"values": ["V1"], "interests": ["I1"], "lifestyle": "Lifestyle"},
    "behaviors": {"online_behavior": "Online", "purchasing_behavior": "Purchase", "media_consumption": "Media"},
    "pain_points": ["Pain1"],
    "goals": ["Goal1"],
    "needs": ["Need1"],
    "preferred_channels": ["Channel1"]
  }],
  "persona_summary": "Summary"
}
"""

