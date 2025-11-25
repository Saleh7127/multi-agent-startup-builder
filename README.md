# Multi-Agent Startup Builder

A multi-agent system designed to take a raw startup idea and evolve it into a comprehensive business plan, pitch deck, and visual identity using Google's Agent Development Kit (ADK) and Gemini models.

## 🚀 Key Features

*   **Advanced Agent Orchestration**:
    *   **Sequential Agents**: For linear workflows (Idea Intake -> Research -> Planning).
    *   **Parallel Agents**: For concurrent execution of Research (Market/Competitor) and Planning (MVP/Tech/Revenue) phases.
    *   **Loop Agents**: For iterative refinement of the Pitch Deck with a VC Critic agent.
*   **Persistent Memory & Sessions**:
    *   **SQLite-based Memory**: Automatically stores and retrieves agent responses across sessions.
    *   **Session Management**: Maintains conversation state and context.
*   **Observability**:
    *   **LoggingPlugin**: Provides detailed, structured logs of agent execution, tool calls, and LLM interactions.
*   **Evaluation Framework**:
    *   Built-in evaluation scripts to assess agent performance against golden datasets.
*   **Rich Tooling**:
    *   **Google Search**: For real-time market data.
    *   **MCP Calculator**: For precise financial projections.
    *   **Custom Tools**: Logo generation and PDF creation.

## 🏗️ Architecture

The system is orchestrated by a **Root Agent** that routes requests to either the **Startup Builder Orchestrator** (for building) or the **Memory Bank Agent** (for querying past data).

For a detailed breakdown of the architecture, agent flows, and future roadmap, please refer to [ARCHITECTURE_PLAN.md](docs/ARCHITECTURE_PLAN.md).

## 🛠️ Prerequisites

*   Python 3.10+
*   Google Gemini API Key

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
    *Note: Make sure to activate the virtual environment before running any commands.*

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