IDEA_INTAKE_PROMPT = """
Analyze the startup idea. Keep responses concise. Return JSON only:

{
  "title": "Title (3-8 words)",
  "description": "1-2 sentences",
  "target_user": "User segment",
  "problem": "Problem (1 sentence)",
  "initial_solution": "Solution (1 sentence)",
  "potential_missing_info": ["Item1", "Item2"]
}
"""