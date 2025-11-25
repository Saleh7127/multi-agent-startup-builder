FINANCIAL_PROJECTIONS_PROMPT = """
Create financial projections. Use mcp_calculator if available. Keep concise. Return JSON only:

{
  "revenue_projections": {
    "year_1": {"revenue": "Amount", "assumptions": ["A1", "A2"], "metrics": ["M1", "M2"]},
    "year_2": {"revenue": "Amount", "growth_rate": "Rate"},
    "year_3": {"revenue": "Amount", "growth_rate": "Rate"}
  },
  "monetization_timeline": {
    "phase_1": {"timeline": "Brief", "approach": "Brief", "goals": ["G1", "G2"]},
    "phase_2": {"timeline": "Brief", "approach": "Brief", "goals": ["G1"]}
  },
  "key_metrics": {
    "revenue_metrics": ["MRR", "ARR"],
    "customer_metrics": ["CAC", "LTV"],
    "growth_metrics": ["M1", "M2"],
    "calculated_metrics": {"roi": "ROI", "payback_period": "Period"}
  },
  "assumptions": {
    "market": ["A1", "A2"],
    "customer": ["A1"],
    "growth": ["A1"],
    "risks": ["R1"]
  }
}
"""

