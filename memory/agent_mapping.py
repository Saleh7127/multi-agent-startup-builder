OUTPUT_KEY_TO_AGENT_NAME = {
    "idea_intake_result": "idea_intake_agent",
    "market_analysis_result": "market_analysis_agent",
    "competitor_research_result": "competitor_research_agent",
    "customer_persona_result": "customer_persona_agent",
    "mvp_feature_planner_result": "mvp_feature_planner_agent",
    "technical_architect_result": "technical_architect_agent",
    "revenue_strategy_result": "revenue_strategy_agent",
    "financial_projections_result": "financial_projections_agent",
    "go_to_market_result": "go_to_market_agent",
    "visual_identity_result": "visual_identity_agent",
    "pitch_deck_result": "pitch_deck_agent",
    "vc_critic_result": "vc_critic_agent",
    "pdf_generation_result": "pdf_generation_agent",
}

def get_agent_name_from_output_key(output_key: str) -> str:
    return OUTPUT_KEY_TO_AGENT_NAME.get(output_key, output_key.replace("_result", "_agent"))

