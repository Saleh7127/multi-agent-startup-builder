GO_TO_MARKET_PROMPT = """
Analyze {idea_intake_result}, {market_analysis_result}, {customer_persona_result}. Use google_search. Return JSON only:

{
  "launch_objectives": ["Goal1"],
  "positioning": {"value_proposition": "VP", "key_messages": ["M1"]},
  "launch_plan": [{"phase": "Pre-launch|Launch|Post-launch", "timeline": "Timeline", "goals": ["G1"], "milestones": ["M1"], "owners": ["Owner1"]}],
  "channel_strategy": [{"channel": "Channel", "tactics": ["T1"], "budget_allocation": "Budget", "primary_metric": "Metric", "notes": "Notes"}],
  "growth_loops": [{"loop_name": "Name", "trigger": "Trigger", "loop_mechanism": "Mechanism", "measurement": "Metric"}],
  "enablement_requirements": ["Req1"],
  "risks_and_mitigations": [{"risk": "Risk", "mitigation": "Mitigation"}],
  "kpi_dashboard": ["KPI1"]
}
"""
