IDEA_INTAKE_PROMPT = """
Analyze the startup idea and return JSON only (no markdown):

{
  "title": "Concise title (3-8 words)",
  "description": "2-3 sentence description",
  "target_user": "Specific user segment",
  "problem": "Problem being solved",
  "initial_solution": "Proposed solution",
  "potential_missing_info": ["Missing details"] // Empty [] if complete
}
"""