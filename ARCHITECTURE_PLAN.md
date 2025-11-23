# Multi-Agent Startup Builder - Architecture Plan

## Executive Summary

This document outlines the improved architecture for the multi-agent startup builder system, incorporating parallel processing, iterative loops, session management, observability, and comprehensive tool integration using Google ADK.

## Current Architecture Analysis

### ✅ Currently Covered Features

1. **LLM-Powered Agents**: All agents use Gemini models via `LlmAgent`
2. **Sequential Agents**: Uses `SequentialAgent` from Google ADK
3. **Custom Tools**: `logo_generation_tool`, `pdf_generation_tool`
4. **MCP Tools**: `mcp_calculator` (Model Context Protocol)
5. **Built-in Tools**: `google_search` from Google ADK
6. **Basic Session Management**: `InMemoryRunner` (implicit session state)

### ❌ Missing Features (To Be Implemented)

1. **Parallel Agents**: `ParallelAgent` from Google ADK
2. **Loop Agents**: `LoopAgent` for iterative refinement
3. **OpenAPI Tools**: Integration with external APIs
4. **Long-Running Operations**: Pause/resume capabilities
5. **Advanced Session Management**: `InMemorySessionService` with explicit session control
6. **Long-Term Memory**: Memory Bank for persistent storage
7. **Context Engineering**: Context compaction techniques
8. **Observability**: Logging, tracing, metrics
9. **Agent Evaluation**: Performance assessment framework
10. **A2A Protocol**: Agent-to-Agent communication protocol

---

## Proposed Improved Architecture

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    IDEA INTAKE AGENT                        │
│                  (Sequential - Entry Point)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              PARALLEL RESEARCH PHASE                        │
│  ┌──────────────────────┐  ┌──────────────────────┐         │
│  │ Market Analysis      │  │ Competitor Research  │         │
│  │ Agent                │  │ Agent                │         │
│  │ Tools: google_search │  │ Tools: google_search │         │
│  └──────────────────────┘  └──────────────────────┘         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              CUSTOMER PERSONA AGENT                         │
│              (Sequential - Synthesizes Research)            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│           PARALLEL PLANNING PHASE                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│  │ MVP Feature  │ │ Technical    │ │ Revenue      │         │ 
│  │ Planner      │ │ Architect    │ │ Strategy     │         │
│  └──────────────┘ └──────────────┘ └──────────────┘         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         SEQUENTIAL EXECUTION PHASE                          │
│  Financial Projections → Go-to-Market → Visual Identity     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│            ITERATIVE REFINEMENT LOOP                        │
│  ┌──────────────────────┐  ┌──────────────────────┐         │
│  │ Pitch Deck Agent     │◄─┤ VC Critic Agent      │         │
│  │                      │  │ (Approval/Feedback)  │         │
│  └──────────────────────┘  └──────────────────────┘         │
│           ▲                         │                       │
│           │                         │                       │
│           └───────── LOOP (2-3 iterations) ─────────┘       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼ (Approved)
┌─────────────────────────────────────────────────────────────┐
│              PDF GENERATION AGENT                           │
│              (Sequential - Final Output)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Detailed Architecture Components

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

## Feature Implementation Plan

### Phase 1: Core Architecture Improvements

#### 1.1 Parallel Agent Implementation
```python
from google.adk.agents import ParallelAgent

# Parallel research phase
parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[
        market_analysis_agent,
        competitor_research_agent,
    ],
)

# Parallel planning phase
parallel_planning_agent = ParallelAgent(
    name="parallel_planning_agent",
    sub_agents=[
        mvp_feature_planner_agent,
        technical_architect_agent,
        revenue_strategy_agent,
    ],
)
```

#### 1.2 Loop Agent Implementation
```python
from google.adk.agents import LoopAgent

# Iterative refinement loop
pitch_refinement_loop = LoopAgent(
    name="pitch_refinement_loop",
    sub_agents=[
        pitch_deck_agent,
        vc_critic_agent,  # NEW agent to be created
    ],
    max_iterations=3,
    exit_condition=lambda state: (
        state.get("vc_critic_result", {}).get("status") == "approved"
        or state.get("iteration_count", 0) >= 3
    ),
)
```

#### 1.3 VC Critic Agent (NEW)
```python
vc_critic_agent = LlmAgent(
    name="vc_critic_agent",
    model=Gemini(model="gemini-2.5-flash", retry_options=retry_config),
    instruction=VC_CRITIC_PROMPT,
    output_key="vc_critic_result",
)
```

**VC Critic Prompt Structure**:
- Evaluate pitch deck completeness
- Assess investor appeal (problem-solution fit, market opportunity, team, traction)
- Check for missing critical sections
- Provide actionable feedback
- Return structured JSON: `{"status": "approved" | "needs_revision", "feedback": [...], "score": 0-100}`

---

### Phase 2: Advanced Session & Memory Management

#### 2.1 InMemorySessionService
```python
from google.adk.sessions import InMemorySessionService
from google.adk.runners import SessionRunner

session_service = InMemorySessionService()
runner = SessionRunner(
    agent=root_agent,
    session_service=session_service,
)
```

**Benefits**:
- Explicit session management
- Session state persistence
- Multi-turn conversation support
- Session cleanup and lifecycle management

#### 2.2 Memory Bank (Long-Term Memory)
```python
from google.adk.memory import MemoryBank

memory_bank = MemoryBank(
    storage_path="memory/storage",
    embedding_model="gemini-2.5-flash-embedding",  # If available
)
```

**Use Cases**:
- Store successful pitch deck patterns
- Learn from previous iterations
- Build knowledge base of startup ideas
- Context retrieval for similar startups

**Integration**:
- Agents can query memory bank for similar cases
- Store successful outputs for future reference
- Learn from VC feedback patterns

#### 2.3 Context Engineering (Context Compaction)
```python
from google.adk.context import ContextCompactor

context_compactor = ContextCompactor(
    max_tokens=32000,  # Model context limit
    strategy="summarize",  # or "truncate", "selective"
)
```

**Implementation**:
- Summarize previous agent outputs when context gets too long
- Maintain key information while reducing token usage
- Selective context retention based on relevance scores
- Automatic context compaction in long-running sessions

---

### Phase 3: Tool Integration Enhancements

#### 3.1 OpenAPI Tools
```python
from google.adk.tools import OpenAPITool

# Example: Integrate with external APIs
crunchbase_api = OpenAPITool(
    openapi_spec_url="https://api.crunchbase.com/openapi.json",
    api_key_env_var="CRUNCHBASE_API_KEY",
)

# Add to relevant agents
competitor_research_agent.tools.append(crunchbase_api)
market_analysis_agent.tools.append(crunchbase_api)
```

**Potential OpenAPI Integrations**:
- Crunchbase API (company/competitor data)
- LinkedIn API (team validation)
- Financial data APIs (market sizing)
- Patent databases (IP research)

#### 3.2 Enhanced MCP Tools
- Expand MCP toolset beyond calculator
- Add MCP tools for:
  - Web scraping (with MCP server)
  - Database queries
  - File operations
  - External service integrations

---

### Phase 4: Long-Running Operations & Observability

#### 4.1 Pause/Resume Capabilities
```python
from google.adk.runners import PausableRunner

pausable_runner = PausableRunner(
    agent=root_agent,
    session_service=session_service,
    checkpoint_dir="checkpoints/",
)

# Usage
session_id = await pausable_runner.start_session(user_input)

# Pause and save state
await pausable_runner.pause_session(session_id)

# Resume later
await pausable_runner.resume_session(session_id)
```

**Use Cases**:
- Handle timeouts and interruptions
- Manual pause/resume for long operations
- Batch processing of multiple startup ideas
- Resource management and cost control

#### 4.2 Observability (Logging, Tracing, Metrics)

**Logging**:
```python
import logging
from google.adk.observability import AgentLogger

agent_logger = AgentLogger(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/agent_execution.log"),
        logging.StreamHandler(),
    ],
)

# Structured logging for each agent execution
agent_logger.log_agent_execution(
    agent_name="market_analysis_agent",
    input_context={...},
    output={...},
    duration=1.23,
    tokens_used=500,
)
```

**Tracing**:
```python
from google.adk.observability import AgentTracer

tracer = AgentTracer(
    exporter="console",  # or "cloud_trace", "jaeger"
    service_name="startup-builder",
)

# Automatic tracing of agent calls
with tracer.span("parallel_research_phase"):
    result = await parallel_research_agent.run(...)
```

**Metrics**:
```python
from google.adk.observability import MetricsCollector

metrics = MetricsCollector()

# Track metrics
metrics.increment("agent.executions", tags={"agent": "market_analysis"})
metrics.histogram("agent.duration", value=1.23, tags={"agent": "market_analysis"})
metrics.gauge("agent.tokens_used", value=500, tags={"agent": "market_analysis"})

# Export metrics (Prometheus, Cloud Monitoring, etc.)
metrics.export(prometheus_port=9090)
```

**Key Metrics to Track**:
- Agent execution time
- Token usage per agent
- Success/failure rates
- Iteration counts (for loop agents)
- Tool call counts and durations
- Context sizes
- Memory bank query performance

---

### Phase 5: Agent Evaluation Framework

#### 5.1 Evaluation Metrics
```python
from google.adk.evaluation import AgentEvaluator

evaluator = AgentEvaluator(
    evaluation_criteria={
        "completeness": lambda output: check_required_fields(output),
        "quality": lambda output: score_quality(output),
        "accuracy": lambda output, expected: compare_outputs(output, expected),
    },
)

# Evaluate agent outputs
score = await evaluator.evaluate(
    agent=market_analysis_agent,
    test_cases=test_data,
)
```

**Evaluation Criteria**:
- **Output Completeness**: All required fields present
- **Output Quality**: Coherence, relevance, detail level
- **Output Accuracy**: Factual correctness (if test data available)
- **Performance**: Execution time, token efficiency
- **Tool Usage**: Appropriate tool selection and utilization

**Test Dataset**:
- Curated startup ideas with expected outputs
- Golden reference outputs for each agent
- Edge cases and failure scenarios

---

### Phase 6: A2A Protocol Implementation

#### 6.1 Agent-to-Agent Communication
```python
from google.adk.protocols.a2a import A2AProtocol

a2a_protocol = A2AProtocol(
    message_bus="memory://",  # or "redis://", "rabbitmq://"
    agent_registry={
        "market_analysis": market_analysis_agent,
        "competitor_research": competitor_research_agent,
        "vc_critic": vc_critic_agent,
    },
)

# Agents can send messages to each other
await a2a_protocol.send_message(
    from_agent="market_analysis",
    to_agent="customer_persona",
    message={"type": "market_insight", "data": {...}},
)
```

**Use Cases**:
- Direct agent-to-agent communication
- Event-driven agent activation
- Cross-agent collaboration
- Decoupled agent architecture

---

## Implementation Roadmap

### ✅ Phase 1: Core Improvements (Week 1-2)
1. Implement ParallelAgent for research phase
2. Implement ParallelAgent for planning phase
3. Create VC Critic Agent
4. Implement LoopAgent for pitch refinement
5. Refactor root_agent.py with new architecture
6. Update prompts for new flow
7. Test new workflow

### 📋 Phase 2: Session & Memory (Week 3)
1. Integrate InMemorySessionService
2. Implement Memory Bank
3. Add context compaction
4. Test session persistence

### 📋 Phase 3: Tool Integration (Week 4)
1. Add OpenAPI tools (Crunchbase, etc.)
2. Enhance MCP toolset
3. Test tool integrations

### 📋 Phase 4: Observability (Week 5)
1. Implement logging framework
2. Add tracing support
3. Implement metrics collection
4. Create monitoring dashboard

### 📋 Phase 5: Evaluation (Week 6)
1. Create evaluation framework
2. Build test dataset
3. Implement evaluation metrics
4. Run baseline evaluations

### 📋 Phase 6: A2A Protocol (Week 7)
1. Implement A2A protocol
2. Enable cross-agent messaging
3. Test event-driven architecture

---

## Updated Root Agent Structure

```python
from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent

# Phase 1: Idea Intake
phase1_intake = idea_intake_agent

# Phase 2: Parallel Research
phase2_research = ParallelAgent(
    name="parallel_research",
    sub_agents=[market_analysis_agent, competitor_research_agent],
)

# Phase 3: Customer Persona
phase3_persona = customer_persona_agent

# Phase 4: Parallel Planning
phase4_planning = ParallelAgent(
    name="parallel_planning",
    sub_agents=[
        mvp_feature_planner_agent,
        technical_architect_agent,
        revenue_strategy_agent,
    ],
)

# Phase 5: Sequential Execution
phase5_execution = SequentialAgent(
    name="sequential_execution",
    sub_agents=[
        financial_projections_agent,
        go_to_market_agent,
        visual_identity_agent,
    ],
)

# Phase 6: Iterative Refinement Loop
phase6_refinement = LoopAgent(
    name="pitch_refinement_loop",
    sub_agents=[pitch_deck_agent, vc_critic_agent],
    max_iterations=3,
    exit_condition=lambda state: (
        state.get("vc_critic_result", {}).get("status") == "approved"
        or state.get("iteration_count", 0) >= 3
    ),
)

# Phase 7: PDF Generation
phase7_output = pdf_generation_agent

# Root agent orchestrates all phases
root_agent = SequentialAgent(
    name="RootAgent",
    description=ROOT_AGENT_WORKFLOW,
    sub_agents=[
        phase1_intake,
        phase2_research,
        phase3_persona,
        phase4_planning,
        phase5_execution,
        phase6_refinement,
        phase7_output,
    ],
)
```

---

## Feature Coverage Matrix

| Feature | Status | Implementation Notes |
|---------|--------|---------------------|
| **Agent Types** |
| LLM-Powered Agents | ✅ Covered | All agents use LlmAgent with Gemini |
| Parallel Agents | ❌ To Implement | Phase 1: ParallelAgent for research & planning |
| Sequential Agents | ✅ Covered | Already using SequentialAgent |
| Loop Agents | ❌ To Implement | Phase 1: LoopAgent for pitch refinement |
| **Tools** |
| MCP Tools | ✅ Covered | mcp_calculator already implemented |
| Custom Tools | ✅ Covered | logo_generation_tool, pdf_generation_tool |
| Built-in Tools | ✅ Covered | google_search from Google ADK |
| OpenAPI Tools | ❌ To Implement | Phase 3: Add external API integrations |
| **Operations** |
| Long-Running (Pause/Resume) | ❌ To Implement | Phase 4: PausableRunner |
| **Sessions & Memory** |
| Session & State Management | ⚠️ Partial | InMemoryRunner → Upgrade to InMemorySessionService (Phase 2) |
| Long-Term Memory | ❌ To Implement | Phase 2: Memory Bank |
| Context Engineering | ❌ To Implement | Phase 2: Context Compaction |
| **Observability** |
| Logging | ❌ To Implement | Phase 4: Structured logging |
| Tracing | ❌ To Implement | Phase 4: Distributed tracing |
| Metrics | ❌ To Implement | Phase 4: Metrics collection |
| **Evaluation** |
| Agent Evaluation | ❌ To Implement | Phase 5: Evaluation framework |
| **Protocols** |
| A2A Protocol | ❌ To Implement | Phase 6: Agent-to-Agent communication |

---

## Benefits of New Architecture

1. **Performance**: Parallel execution reduces total execution time by ~40-50%
2. **Quality**: Iterative VC critic loop ensures pitch deck meets investor standards
3. **Scalability**: Memory bank and session management support multiple concurrent requests
4. **Observability**: Comprehensive logging, tracing, and metrics enable debugging and optimization
5. **Flexibility**: A2A protocol enables event-driven and decoupled architectures
6. **Reliability**: Pause/resume capabilities handle long-running operations gracefully
7. **Continuous Improvement**: Evaluation framework enables systematic quality improvement

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Google ADK API limitations/changes | Monitor ADK documentation, implement fallbacks |
| Parallel agent coordination issues | Test thoroughly, implement proper error handling |
| Loop agent infinite loops | Strict max_iterations limit, timeout mechanisms |
| Memory bank storage overhead | Implement cleanup policies, use efficient storage |
| Context compaction losing information | Careful summarization strategies, key information preservation |
| Tool integration failures | Graceful degradation, retry mechanisms |
| Evaluation framework maintenance | Automated test generation, CI/CD integration |

---

## Conclusion

This architecture plan provides a comprehensive roadmap for enhancing the multi-agent startup builder system with advanced features including parallel processing, iterative refinement, session management, observability, and evaluation capabilities. The phased implementation approach allows for incremental improvements while maintaining system stability.

**Estimated Timeline**: 6-7 weeks for full implementation
**Priority**: Phase 1 (Core Improvements) is critical and should be implemented first
**Dependencies**: Google ADK feature availability (ParallelAgent, LoopAgent, Memory Bank, etc.)

