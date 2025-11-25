MVP_FEATURE_PLANNER_PROMPT = """
Plan MVP features. Keep concise. Return JSON only:

{
  "mvp_vision": "1 sentence",
  "core_features": [{"feature_name": "Name", "description": "Brief", "priority": "Must Have|Should Have", "user_value": "Brief", "complexity": "Low|Medium|High"}],
  "feature_prioritization": {"phase_1_mvp": ["F1", "F2", "F3"], "phase_2": ["F4", "F5"]},
  "mvp_scope": {"in_scope": ["Item1", "Item2"], "out_of_scope": ["Item1"], "rationale": "Brief"},
  "success_metrics": {"key_metrics": ["M1", "M2", "M3"], "goals": ["G1", "G2"]}
}
"""

