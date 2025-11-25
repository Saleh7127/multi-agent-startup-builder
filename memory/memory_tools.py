import json
from typing import Optional
from google.adk.tools import FunctionTool
from .memory_config import memory_service


def store_agent_response(
    app_name: str,
    user_id: str,
    session_id: str,
    agent_name: str,
    response_json: str,
) -> dict:
    try:
        if user_id is None or session_id is None:
            return {"status": "error", "message": "user_id and session_id required"}
        memory_service.store_agent_response(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            agent_name=agent_name,
            response_json=response_json,
        )
        return {"status": "success", "message": f"Stored {agent_name} response"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_agent_response(
    agent_name: str,
    app_name: str = "startup-builder",
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
) -> dict:
    try:
        if user_id is None or session_id is None:
            return {"status": "error", "message": "user_id and session_id required"}
        response = memory_service.get_agent_response(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            agent_name=agent_name,
        )
        if response:
            return {"status": "success", "response_json": response}
        return {"status": "not_found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_session_responses(
    app_name: str,
    user_id: str,
    session_id: str,
) -> dict:
    try:
        responses = memory_service.get_session_responses(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )
        return {"status": "success", "responses": responses}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_latest_agent_response(
    agent_name: str,
    app_name: str = "startup-builder",
    user_id: Optional[str] = None,
    limit: int = 1,
) -> dict:
    """
    Get the latest response from a specific agent from memory.
    
    Args:
        agent_name: Name of the agent (e.g., "idea_intake_agent", "market_analysis_agent")
        app_name: Application name (default: "startup-builder")
        user_id: Optional user ID to filter by specific user. If None, searches all users.
        limit: Number of results to return (default: 1)
    
    Returns:
        dict with status ("success", "not_found", or "error"), and if successful:
        - agent_name: The agent name
        - response_json: The agent's response content
        - session_id: The session ID where this response was stored
        - created_at: When it was created
    """
    try:
        results = memory_service.search_responses(
            agent_name=agent_name,
            app_name=app_name,
            user_id=user_id,
            limit=limit,
        )
        if results:
            latest = results[0]
            return {
                "status": "success",
                "agent_name": latest["agent_name"],
                "response_json": latest["response_json"],
                "session_id": latest["session_id"],
                "created_at": latest["created_at"],
            }
        return {
            "status": "not_found", 
            "message": f"No response found for agent '{agent_name}'. The database may be empty or this agent hasn't run yet.",
            "agent_name": agent_name
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


get_latest_tool = FunctionTool(get_latest_agent_response)
get_response_tool = FunctionTool(get_agent_response)
get_session_tool = FunctionTool(get_session_responses)

MEMORY_TOOLS = [
    get_latest_tool,
    get_response_tool,
    get_session_tool,
]
