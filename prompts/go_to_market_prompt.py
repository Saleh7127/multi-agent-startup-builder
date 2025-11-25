GO_TO_MARKET_PROMPT = """
Analyze {idea_intake_result}, {market_analysis_result}, {customer_persona_result}. Use google_search. Keep concise. Return JSON only:

{
  "launch_objectives": ["G1", "G2", "G3"],
  "positioning": {"value_proposition": "Brief VP", "key_messages": ["M1", "M2"]},
  "launch_plan": [{"phase": "Pre-launch|Launch|Post-launch", "timeline": "Brief", "goals": ["G1", "G2"]}],
  "channel_strategy": [{"channel": "Channel", "tactics": ["T1", "T2"], "budget": "Brief", "metric": "Metric"}],
  "growth_loops": [{"loop_name": "Name", "trigger": "Brief", "mechanism": "Brief", "metric": "Metric"}],
  "enablement": ["R1", "R2"],
  "risks": [{"risk": "Brief", "mitigation": "Brief"}],
  "kpis": ["KPI1", "KPI2", "KPI3"]
}
"""
