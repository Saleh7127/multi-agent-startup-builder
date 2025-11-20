MVP_FEATURE_PLANNER_PROMPT = """
Plan MVP features. Return JSON only:

{
  "mvp_vision": "Vision statement",
  "core_features": [{"feature_name": "Name", "description": "Desc", "priority": "Must Have|Should Have|Nice to Have", "user_value": "Value", "complexity": "Low|Medium|High", "dependencies": ["Dep1"]}],
  "feature_prioritization": {"phase_1_mvp": ["Feature1"], "phase_2": ["Feature2"], "phase_3": ["Feature3"]},
  "mvp_scope": {"in_scope": ["In1"], "out_of_scope": ["Out1"], "rationale": "Rationale"},
  "success_metrics": {"validation_criteria": ["Crit1"], "key_metrics": ["Metric1"], "goals": ["Goal1"]}
}
"""

