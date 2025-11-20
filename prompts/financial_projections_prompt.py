FINANCIAL_PROJECTIONS_PROMPT = """
Create financial projections. Use mcp_calculator if available. Return JSON only:

{
  "revenue_projections": {
    "year_1": {"estimated_revenue": "Revenue", "assumptions": ["A1"], "key_metrics": ["M1"], "breakdown": "Breakdown"},
    "year_2": {"estimated_revenue": "Revenue", "assumptions": ["A1"], "growth_rate": "Rate"},
    "year_3": {"estimated_revenue": "Revenue", "assumptions": ["A1"], "growth_rate": "Rate"}
  },
  "monetization_timeline": {
    "phase_1": {"timeline": "Timeline", "approach": "Approach", "goals": ["G1"], "milestones": ["M1"]},
    "phase_2": {"timeline": "Timeline", "approach": "Approach", "goals": ["G1"], "milestones": ["M1"]}
  },
  "key_metrics": {
    "revenue_metrics": ["MRR", "ARR"],
    "customer_metrics": ["CAC", "LTV"],
    "growth_metrics": ["Metric1"],
    "profitability_metrics": ["Metric1"],
    "calculated_metrics": {"roi": "ROI", "payback_period": "Period", "growth_rates": "Rates", "other_ratios": ["Ratio1"]}
  },
  "financial_assumptions": {
    "market_assumptions": ["A1"],
    "customer_assumptions": ["A1"],
    "growth_assumptions": ["A1"],
    "risk_factors": ["R1"]
  }
}
"""

