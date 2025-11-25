# Multi-Agent Startup Builder

A comprehensive multi-agent system designed to take a raw startup idea and evolve it into a polished business plan, pitch deck, and visual identity using Google's Agent Development Kit (ADK) and Gemini models.

## � The Problem

Startup founders often face a daunting and complex process when preparing for pitches or analyzing the market. They must navigate a multitude of tasks—from deep market research and competitor analysis to financial modeling and pitch deck creation. This manual process is time-consuming, prone to oversight, and can be overwhelming for early-stage entrepreneurs. This system aims to solve that issue by automating these critical steps, allowing founders to focus on their vision.

## 💡 The Solution

The **Multi-Agent Startup Builder** leverages the power of Large Language Models (LLMs) to act as an intelligent co-founder. It orchestrates a team of specialized AI agents that work in parallel and sequentially to:

1.  **Validate Ideas**: Refine and structure raw concepts.
2.  **Conduct Research**: Perform deep-dive market and competitor analysis using real-time data.
3.  **Plan Strategically**: Define MVPs, technical architectures, and revenue models.
4.  **Execute**: Generate financial projections, go-to-market strategies, and visual assets.
5.  **Refine**: Iteratively improve pitch decks based on simulated VC feedback.

## 🏗️ Architecture

The system is built on a robust architecture that orchestrates multiple specialized agents. It features a **Root Agent** for routing, a **Startup Builder Orchestrator** for managing the build pipeline, and a **Memory Bank** for context retention.

### Architecture Diagram

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

### Core Components

*   **Root Agent**: The entry point that routes user requests to either the Builder or Memory services.
*   **Startup Builder Orchestrator**: Manages the lifecycle of the startup creation process.
*   **Parallel Agents**: Executes independent tasks (like Market Analysis and Competitor Research) simultaneously for efficiency.
*   **Loop Agents**: Implements a feedback loop where a "VC Critic" agent reviews the pitch deck and requests revisions until it meets quality standards.
*   **Memory Service**: Uses SQLite to persist agent outputs and session state, allowing for long-term context retention.

## 🚀 Key Features

*   **Advanced Agent Orchestration**:
    *   **Sequential Agents**: For linear workflows.
    *   **Parallel Agents**: For concurrent execution of research and planning phases.
    *   **Loop Agents**: For iterative refinement.
*   **Persistent Memory & Sessions**:
    *   **SQLite-based Memory**: Automatically stores and retrieves agent responses.
    *   **Session Management**: Maintains conversation state.
*   **Observability**:
    *   **LoggingPlugin**: Provides detailed, structured logs of agent execution and tool calls.
*   **Evaluation Framework**:
    *   Built-in evaluation scripts to assess agent performance.
*   **Rich Tooling**:
    *   **Google Search**: For real-time market data.
    *   **MCP Calculator**: For precise financial projections.
    *   **Custom Tools**: Logo generation and PDF creation.

## 🛠️ Prerequisites

*   **Python 3.10+**
*   **Google Gemini API Key**

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd multi-agent-startup-builder
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: For full evaluation capabilities, you may need `pip install "google-adk[eval]"`.*

4.  **Configure Environment**:
    Create a `.env` file in the root directory and add your API keys:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key
    ```

## 🏃‍♂️ Usage

### Build a Startup
To start the startup builder pipeline with an initial idea:

```bash
python main.py "I want to build a platform for connecting dog walkers with owners."
```

By using adk web - 
```bash
adk web
```

By using adk cli - 
```bash
adk run agents
```

The system will guide you through:
1.  **Idea Intake**: Refining your concept.
2.  **Research**: Analyzing the market and competitors (Parallel).
3.  **Planning**: Defining MVP, Tech Stack, and Revenue Strategy (Parallel).
4.  **Execution**: Financials, GTM Strategy, and Visual Identity.
5.  **Refinement**: Iteratively improving the pitch deck with VC feedback.
6.  **Output**: Generating a final PDF pitch deck.

### Run Evaluation
To evaluate the agents (e.g., `idea_intake_agent`) against test cases:

```bash
python tests/run_eval.py
```

## 📂 Project Structure

*   `agents/`: Definitions for all agents (Idea Intake, Market Analysis, etc.).
*   `generated_assets/`: Output directory for Pitch Decks and Logos.
*   `memory/`: Memory services (`SqliteMemoryService`) and callbacks.
*   `prompts/`: System instructions and prompts for each agent.
*   `tests/`: Evaluation scripts and test data.
*   `tools/`: Custom tools (Logo, PDF) and MCP integrations.
*   `utils/`: Utility functions for retry configuration.
*   `main.py`: Entry point for the application.

## 🔍 Observability

The system uses a `LoggingPlugin` to output detailed execution traces to the console. This helps in debugging agent flows, understanding tool usage, and monitoring LLM token consumption.