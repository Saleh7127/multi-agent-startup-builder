"""
ROOT Agent Orchestration Prompt

This document describes the multi-agent workflow orchestrated by the ROOT Agent.
The ROOT Agent uses Google ADK's SequentialAgent to execute all agents in sequence,
with each agent's output available to subsequent agents via {output_key} placeholders.
"""

ROOT_AGENT_WORKFLOW = """
# Multi-Agent Startup Builder - Agent Orchestration Workflow

## Overview
The Root Agent orchestrates a sequential pipeline of 12 specialized agents to transform a raw startup idea into a comprehensive PDF pitch deck.
## Agent Execution Flow

### 1. `idea_intake_agent`
**Input:** Raw startup idea (user input)
**Duty:** 
- Analyze and structure the raw startup idea
- Extract core problem, solution, and target user
- Identify missing information
- Create structured JSON summary

**Output Key:** `idea_intake_result`
**Output Format:** JSON with title, description, target_user, problem, initial_solution, potential_missing_info

**Available to Next Agents:** {idea_intake_result}

---

### 2. Market Analysis Agent
**Input:** {idea_intake_result} (from `idea_intake_agent`)
**Duty:**
- Conduct comprehensive market research using google_search tool
- Analyze market size (TAM/SAM)
- Identify market trends and opportunities
- Assess market challenges and growth potential
- Determine market maturity stage

**Output Key:** `market_analysis_result`
**Output Format:** JSON with market_size, market_trends, market_opportunities, market_challenges, target_segments, growth_potential, market_maturity

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}

---

### 3. Competitor Research Agent
**Input:** {idea_intake_result} (from `idea_intake_agent`)
**Duty:**
- Identify direct and indirect competitors using google_search tool
- Analyze competitor business models, strengths, and weaknesses
- Assess competitive landscape and market positioning
- Identify market gaps and differentiation opportunities

**Output Key:** `competitor_research_result`
**Output Format:** JSON with direct_competitors, indirect_competitors, competitive_landscape, market_gaps, differentiation_opportunities

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}

---

### 4. Customer Persona Agent
**Input:** {idea_intake_result} (from `idea_intake_agent`), {market_analysis_result} (from `market_analysis_agent`)
**Duty:**
- Create 3-5 detailed customer personas
- Define demographics, psychographics, and behaviors
- Identify pain points, goals, and needs
- Determine preferred communication channels

**Output Key:** `customer_persona_result`
**Output Format:** JSON with personas array and persona_summary

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}

---

### 5. MVP Feature Planner Agent
**Input:** {idea_intake_result} (from `idea_intake_agent`), {customer_persona_result} (from `customer_persona_agent`)
**Duty:**
- Define MVP features and functionality
- Prioritize features based on customer needs
- Create product roadmap
- Identify technical requirements

**Output Key:** `mvp_feature_planner_result`
**Output Format:** JSON with MVP features, priorities, roadmap, and technical requirements

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}

---

### 6. Technical Architect Agent
**Input:** {mvp_feature_planner_result} (from `mvp_feature_planner_agent`)
**Duty:**
- Design technical architecture
- Select technology stack
- Define system components and infrastructure
- Plan scalability and performance considerations

**Output Key:** `technical_architect_result`
**Output Format:** JSON with architecture details, tech stack, components, and infrastructure

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}

---

### 7. Revenue Strategy Agent
**Input:** {idea_intake_result} (from `idea_intake_agent`), {market_analysis_result} (from `market_analysis_agent`), {customer_persona_result} (from `customer_persona_agent`)
**Duty:**
- Define revenue model and pricing strategy
- Identify monetization opportunities
- Plan pricing tiers and packages
- Assess revenue potential

**Output Key:** `revenue_strategy_result`
**Output Format:** JSON with revenue model, pricing strategy, monetization plan, and revenue projections

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}

---

### 8. Financial Projections Agent
**Input:** {revenue_strategy_result} (from `revenue_strategy_agent`)
**Duty:**
- Create financial projections and forecasts
- Calculate burn rate and runway
- Project revenue growth
- Estimate funding requirements
- Use mcp_calculator tool for financial calculations

**Output Key:** `financial_projections_result`
**Output Format:** JSON with financial projections, burn rate, runway, revenue forecasts, and funding needs

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}, {financial_projections_result}

---

### 9. Go-to-Market Agent
**Input:** {idea_intake_result} (from `idea_intake_agent`), {market_analysis_result} (from `market_analysis_agent`), {customer_persona_result} (from `customer_persona_agent`)
**Duty:**
- Design go-to-market strategy
- Identify marketing channels and tactics
- Create launch plan with phases
- Define growth loops
- Plan enablement requirements
- Use google_search tool for market insights

**Output Key:** `go_to_market_result`
**Output Format:** JSON with launch objectives, positioning, launch plan, channel strategy, growth loops, enablement requirements, risks, and KPIs

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}, {financial_projections_result}, {go_to_market_result}

---

### 10. Visual Identity Agent
**Input:** {idea_intake_result} (from `idea_intake_agent`)
**Duty:**
- Create visual identity and branding
- Generate logo using logo generation tool
- Define color palette and design guidelines
- Establish brand tone and voice

**Output Key:** `visual_identity_result`
**Output Format:** JSON with logo assets, color palette, design guidelines, and brand tone

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}, {financial_projections_result}, {go_to_market_result}, {visual_identity_result}

---

### 11. Pitch Deck Agent
**Input:** All previous agent outputs:
- {idea_intake_result}
- {market_analysis_result}
- {competitor_research_result}
- {customer_persona_result}
- {mvp_feature_planner_result}
- {technical_architect_result}
- {revenue_strategy_result}
- {financial_projections_result}
- {go_to_market_result}
- {visual_identity_result}

**Duty:**
- Synthesize all agent outputs into investor-ready pitch deck
- Create structured JSON with company info, sections, metrics, investment ask

**Output Key:** `pitch_deck_result`
**Output Format:** JSON with company_name, tagline, elevator_pitch, sections, metrics_snapshot, investment_ask, call_to_action, risks_or_diligence, appendix_notes

**Available to Next Agents:** {idea_intake_result}, {market_analysis_result}, {competitor_research_result}, {customer_persona_result}, {mvp_feature_planner_result}, {technical_architect_result}, {revenue_strategy_result}, {financial_projections_result}, {go_to_market_result}, {visual_identity_result}, {pitch_deck_result}

---

### 12. PDF Generation Agent
**Input:** {pitch_deck_result} (from `pitch_deck_agent`)

**Duty:**
- Extract pitch deck JSON from {pitch_deck_result}
- Generate PDF pitch deck using pdf_generation_tool
- Save PDF to generated_assets/pitch_decks/

**Output Key:** `pdf_generation_result`
**Output Format:** Dictionary with saved_file path and notes

**Final Output:** PDF pitch deck file saved to generated_assets/pitch_decks/

---

## Key Principles

1. **Sequential Execution:** Agents execute in strict order, with each agent receiving outputs from all previous agents
2. **Output Availability:** All previous agent outputs are available via {output_key} placeholders
3. **Data Flow:** Each agent can access and use data from any previous agent in the pipeline
4. **Tool Usage:** Some agents use tools (google_search, mcp_calculator, logo_generation_tool, pdf_generation_tool) to enhance their capabilities
5. **Final Output:** The pipeline culminates in a comprehensive PDF pitch deck ready for investor presentation

## Execution Notes

- The ROOT Agent uses Google ADK's SequentialAgent to manage the execution flow
- Each agent's output is automatically stored in session state with its output_key
- Subsequent agents can reference previous outputs using {output_key} syntax in their instructions
- The entire pipeline runs automatically from a single startup idea input
"""

