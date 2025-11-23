import asyncio
import sys
import uuid
import json
from pathlib import Path
from dotenv import load_dotenv
from google.adk.runners import Runner, types

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.root_agent import root_agent
from memory import session_service, memory_service
from memory.agent_mapping import get_agent_name_from_output_key

load_dotenv()

APP_NAME = "startup-builder"
DEFAULT_USER_ID = "default"


async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py '<startup_idea>' [user_id] [session_id]")
        sys.exit(1)
    
    startup_idea = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_USER_ID
    session_id = sys.argv[3] if len(sys.argv) > 3 else str(uuid.uuid4())
    
    print(f"🚀 Starting Multi-Agent Startup Builder...")
    print(f"📝 Idea: {startup_idea}")
    print(f"👤 User: {user_id}")
    print(f"🔑 Session: {session_id}\n")
    
    try:
        session_service.create_session_sync(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
    except Exception:
        pass
    
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
        memory_service=memory_service,
    )
    
    stored_outputs = set()
    
    try:
        message = types.Content(parts=[types.Part(text=startup_idea)])
        event_gen = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message,
        )
        
        try:
            async for event in event_gen:
                if hasattr(event, 'agent_state') and event.agent_state:
                    state = event.agent_state
                    if hasattr(state, 'to_dict'):
                        state_dict = state.to_dict()
                        for output_key, value in state_dict.items():
                            if output_key.endswith('_result') and output_key not in stored_outputs and value:
                                agent_name = get_agent_name_from_output_key(output_key)
                                try:
                                    if isinstance(value, str):
                                        response_str = value
                                    elif isinstance(value, dict):
                                        response_str = json.dumps(value, ensure_ascii=False)
                                    else:
                                        response_str = str(value)
                                    
                                    if response_str and response_str.strip():
                                        memory_service.store_agent_response(
                                            app_name=APP_NAME,
                                            user_id=user_id,
                                            session_id=session_id,
                                            agent_name=agent_name,
                                            response_json=response_str,
                                        )
                                        stored_outputs.add(output_key)
                                        print(f"💾 Stored: {agent_name}")
                                except Exception as e:
                                    print(f"⚠️  Error storing {agent_name}: {e}")
        finally:
            try:
                await event_gen.aclose()
            except Exception:
                pass
        
        session = session_service.get_session_sync(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )
        
        if session and hasattr(session, 'state') and session.state:
            state = session.state
            if hasattr(state, 'to_dict'):
                state_dict = state.to_dict()
                for output_key, value in state_dict.items():
                    if output_key.endswith('_result') and output_key not in stored_outputs and value:
                        agent_name = get_agent_name_from_output_key(output_key)
                        try:
                            if isinstance(value, str):
                                response_str = value
                            elif isinstance(value, dict):
                                response_str = json.dumps(value, ensure_ascii=False)
                            else:
                                response_str = str(value)
                            
                            if response_str and response_str.strip():
                                memory_service.store_agent_response(
                                    app_name=APP_NAME,
                                    user_id=user_id,
                                    session_id=session_id,
                                    agent_name=agent_name,
                                    response_json=response_str,
                                )
                                stored_outputs.add(output_key)
                                print(f"💾 Stored (final): {agent_name}")
                        except Exception as e:
                            print(f"⚠️  Error storing {agent_name}: {e}")
        
        print("\n✅ Process completed!")
        print(f"💾 Responses stored: {len(stored_outputs)} agents")
        print(f"📁 Database: memory/agent_responses.db")
        
    except Exception as e:
        error_str = str(e)
        error_type = type(e).__name__
        if ("cancel scope" in error_str.lower() or 
            "mcp" in error_str.lower() or 
            "ExceptionGroup" in error_type or
            "BaseExceptionGroup" in error_type):
            print("\n⚠️  MCP cleanup warning (non-critical)")
            print("✅ Process completed")
        else:
            raise


if __name__ == "__main__":
    asyncio.run(main())

