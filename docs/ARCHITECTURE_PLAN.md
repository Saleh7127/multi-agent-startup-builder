# Multi-Agent Startup Builder - Agents Architecture

## Executive Summary

This document outlines the improved architecture for the multi-agent startup builder system, incorporating parallel processing, iterative loops, session management, observability, and comprehensive tool integration using Google ADK.

## Current Architecture Analysis

### ✅ Currently Covered Features

1. **LLM-Powered Agents**: All agents use Gemini models via `LlmAgent`
2. **Sequential Agents**: Uses `SequentialAgent` from Google ADK
3. **Parallel Agents**: `ParallelAgent` implemented for Research and Planning phases
4. **Loop Agents**: `LoopAgent` implemented for Pitch Refinement
5. **Custom Tools**: `logo_generation_tool`, `pdf_generation_tool`
6. **MCP Tools**: `mcp_calculator` (Model Context Protocol)
7. **Built-in Tools**: `google_search` from Google ADK
8. **Session Management**: `DatabaseSessionService` (SQLite) for persistent sessions
9. **Memory**: `SqliteMemoryService` for persistent agent response storage
10. **Observability**: `LoggingPlugin` for detailed execution logs
11. **Agent Evaluation**: Basic infrastructure and `simple_eval.py` verification
12. **VC Critic Agent**: Implemented for feedback loop

### ❌ Missing Features (To Be Implemented)

1. **OpenAPI Tools**: Integration with external APIs
2. **Long-Running Operations**: Pause/resume capabilities
3. **Long-Term Memory**: Advanced Memory Bank with embeddings (Basic persistence exists)
4. **Context Engineering**: Context compaction techniques
5. **A2A Protocol**: Agent-to-Agent communication protocol

---

## Proposed Improved Architecture

### Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                             ROOT AGENT                                   │
│                     (Routes to Memory or Builder)                        │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   │
          ┌────────────────────────┴────────────────────────┐
          ▼                                                 ▼
┌──────────────────────────┐              ┌────────────────────────────────┐
│    MEMORY BANK AGENT     │              │   STARTUP BUILDER ORCHESTRATOR │
│ (Queries Past Responses) │              │      (Manages Build Pipeline)  │
└──────────────────────────┘              └────────────────┬───────────────┘
                                                           │
                                                           ▼
                                   ┌───────────────────────────────────────┐
                                   │           IDEA INTAKE AGENT           │
                                   │        (Sequential - Entry Point)     │
                                   └───────────────────┬───────────────────┘
                                                       │
                                                       ▼
                                   ┌───────────────────────────────────────┐
                                   │         PARALLEL RESEARCH PHASE       │
                                   │  ┌──────────────┐  ┌───────────────┐  │
                                   │  │ Market       │  │ Competitor    │  │
                                   │  │ Analysis     │  │ Research      │  │
                                   │  └──────────────┘  └───────────────┘  │
                                   └───────────────────┬───────────────────┘
                                                       │
                                                       ▼
                                   ┌───────────────────────────────────────┐
                                   │        CUSTOMER PERSONA AGENT         │
                                   │        (Synthesizes Research)         │
                                   └───────────────────┬───────────────────┘
                                                       │
                                                       ▼
                                   ┌───────────────────────────────────────┐
                                   │         PARALLEL PLANNING PHASE       │
                                   │ ┌────────────┐ ┌───────────┐ ┌──────┐ │
                                   │ │ MVP        │ │ Tech      │ │ Rev  │ │
                                   │ │ Planner    │ │ Architect │ │ Strat│ │
                                   │ └────────────┘ └───────────┘ └──────┘ │
                                   └───────────────────┬───────────────────┘
                                                       │
                                                       ▼
                                   ┌───────────────────────────────────────┐
                                   │       SEQUENTIAL EXECUTION PHASE      │
                                   │ Financial → Go-to-Market → Visual ID  │
                                   └───────────────────┬───────────────────┘
                                                       │
                                                       ▼
                                   ┌───────────────────────────────────────┐
                                   │       ITERATIVE REFINEMENT LOOP       │
                                   │ ┌──────────────┐    ┌──────────────┐  │
                                   │ │ Pitch Deck   │◄───┤  VC Critic   │  │
                                   │ └──────────────┘    └──────────────┘  │
                                   └───────────────────┬───────────────────┘
                                                       │
                                                       ▼ (Approved)
                                   ┌───────────────────────────────────────┐
                                   │         PDF GENERATION AGENT          │
                                   │         (Final Output)                │
                                   └───────────────────────────────────────┘
```

---

## Detailed Architecture Components

### 0. System Entry: Root Agent & Routing
- **Root Agent**: The main entry point that routes user requests.
  - **Routes to**:
    - `Memory Bank Agent`: If the user asks a question about past sessions or data.
    - `Startup Builder Orchestrator`: If the user wants to build a startup or perform a task.

- **Memory Bank Agent**:
  - **Purpose**: Retrieves information from the `agent_responses.db` and `sessions.db`.
  - **Tools**: `get_latest_agent_response`, `get_agent_response`.

- **Startup Builder Orchestrator**:
  - **Purpose**: Manages the end-to-end startup building pipeline.
  - **Contains**: All sub-agents listed below (Idea Intake, Research, Planning, etc.).

### 1. Entry Phase: Idea Intake
- **Agent Type**: `LlmAgent` (Sequential)
- **Input**: Raw startup idea (user input)
- **Output**: `idea_intake_result`
- **Purpose**: Structure and validate the initial idea
- **Dependencies**: None

### 2. Parallel Research Phase
- **Agent Type**: `ParallelAgent`
- **Sub-agents**:
  - **Market Analysis Agent**
    - Tools: `google_search`
    - Output: `market_analysis_result`
  - **Competitor Research Agent**
    - Tools: `google_search`
    - Output: `competitor_research_result`
- **Purpose**: Concurrent market and competitor research for efficiency
- **Dependencies**: `idea_intake_result`

### 3. Customer Persona Synthesis
- **Agent Type**: `LlmAgent` (Sequential)
- **Input**: `idea_intake_result`, `market_analysis_result`, `competitor_research_result`
- **Output**: `customer_persona_result`
- **Purpose**: Create customer personas from research insights
- **Dependencies**: Parallel research phase outputs

### 4. Parallel Planning Phase
- **Agent Type**: `ParallelAgent`
- **Sub-agents**:
  - **MVP Feature Planner**
    - Input: `idea_intake_result`, `customer_persona_result`
    - Output: `mvp_feature_planner_result`
  - **Technical Architect**
    - Input: `idea_intake_result`, `customer_persona_result`, `mvp_feature_planner_result` (via context)
    - Output: `technical_architect_result`
  - **Revenue Strategy**
    - Input: `idea_intake_result`, `market_analysis_result`, `customer_persona_result`
    - Output: `revenue_strategy_result`
- **Purpose**: Concurrent planning of product, tech, and business strategy
- **Dependencies**: `customer_persona_result`

### 5. Sequential Execution Phase
- **Agent Type**: `SequentialAgent`
- **Sub-agents** (in order):
  1. **Financial Projections Agent**
     - Tools: `mcp_calculator`
     - Input: `revenue_strategy_result`
     - Output: `financial_projections_result`
  
  2. **Go-to-Market Agent**
     - Tools: `google_search`
     - Input: `idea_intake_result`, `market_analysis_result`, `customer_persona_result`
     - Output: `go_to_market_result`
  
  3. **Visual Identity Agent**
     - Tools: `logo_generation_tool`
     - Input: `idea_intake_result`
     - Output: `visual_identity_result`
- **Purpose**: Sequential execution where each depends on previous outputs or parallel results

### 6. Iterative Refinement Loop
- **Agent Type**: `LoopAgent`
- **Configuration**:
  - Max iterations: 3
  - Exit condition: VC Critic approval (`status: "approved"`)
  - Loop sub-agents:
    1. **Pitch Deck Agent**
       - Input: All previous agent outputs
       - Output: `pitch_deck_result`
       - Creates initial/updated pitch deck
    
    2. **VC Critic Agent** (NEW)
       - Input: `pitch_deck_result`
       - Output: `vc_critic_result`
       - Contains: `status` ("approved" | "needs_revision"), `feedback` (list of improvements)
       - Evaluates pitch deck quality, investor appeal, completeness
- **Purpose**: Iterative refinement until pitch deck meets VC standards
- **Iteration Logic**:
  - If `status == "approved"`: Exit loop, proceed to PDF generation
  - If `status == "needs_revision"` and `iteration_count < 3`: Update pitch deck with feedback
  - If `iteration_count >= 3`: Exit with best available version (with warning)

### 7. Final Output Phase
- **Agent Type**: `LlmAgent` (Sequential)
- **Agent**: PDF Generation Agent
- **Tools**: `pdf_generation_tool`
- **Input**: Final approved `pitch_deck_result`
- **Output**: PDF file in `generated_assets/pitch_decks/`
- **Purpose**: Generate final PDF document

---
