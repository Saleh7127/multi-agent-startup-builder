"""
Google Search Agent - A dedicated agent for performing web searches using Google Search tool.
This agent can be wrapped with AgentTool and used by other agents.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.retryConfig import retry_config

load_dotenv()

GOOGLE_SEARCH_AGENT_PROMPT = """
You are a Google Search Agent specialized in performing web searches to gather current information.

Your primary task is to use the google_search tool to find relevant, up-to-date information based on search queries.

**Instructions:**
1. When given a search query, use the google_search tool to find relevant information
2. Analyze the search results and extract key information
3. Provide a clear summary of the findings
4. Cite sources when possible

**Guidelines:**
- Use the google_search tool for all search operations
- Be specific with search queries to get relevant results
- Summarize findings clearly and concisely
- Include relevant URLs or sources when available
"""

google_search_agent = Agent(
    name="google_search_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction=GOOGLE_SEARCH_AGENT_PROMPT,
    tools=[google_search],
    output_key="search_result",
)

