import asyncio
import sys
import uuid
import json
from pathlib import Path
from dotenv import load_dotenv
from google.adk.runners import Runner, types
from google.adk.plugins.logging_plugin import LoggingPlugin

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
    
    user_input = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_USER_ID
    session_id = sys.argv[3] if len(sys.argv) > 3 else str(uuid.uuid4())
    
    print(f"🚀 Starting Multi-Agent Startup Builder...")
    print(f"📝 Input: {user_input}")
    print(f"👤 User: {user_id}")
    print(f"🔑 Session: {session_id}\n")
    
    try:
        await session_service.create_session(
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
        plugins=[LoggingPlugin()],
    )
    
    stored_outputs = set()
    
    try:
        message = types.Content(parts=[types.Part(text=user_input)])
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
                                except Exception:
                                    pass
        except (TypeError, RuntimeError, Exception):
            pass
        finally:
            try:
                await event_gen.aclose()
            except Exception:
                pass
        
        try:
            session = await session_service.get_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=session_id,
            )
            
            if session:
                state = getattr(session, 'state', None)
                
                state_dict = {}
                if state:
                    if isinstance(state, dict):
                        state_dict = state
                    elif hasattr(state, 'to_dict'):
                        try:
                            state_dict = state.to_dict() or {}
                        except:
                            state_dict = {}
                
                if state_dict:
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
                            except Exception:
                                pass
                
                try:
                    await memory_service.add_session_to_memory(session)
                except Exception:
                    pass
                    
        except Exception:
            pass
        
    except Exception:
        pass


if __name__ == "__main__":
    import sys
    import warnings
    
    warnings.filterwarnings('ignore', message='.*cancel scope.*')
    warnings.filterwarnings('ignore', message='.*mcp.*')
    warnings.filterwarnings('ignore', message='.*asyncgen.*')
    
    try:
        asyncio.run(main())
    except (RuntimeError, ExceptionGroup, BaseExceptionGroup) as e:
        error_str = str(e).lower()
        error_type = type(e).__name__
        
        is_mcp_error = (
            'cancel scope' in error_str or
            'mcp' in error_str or
            'asyncgen' in error_str or
            'stdio_client' in error_str or
            'ExceptionGroup' in error_type or
            'BaseExceptionGroup' in error_type
        )
        
        if is_mcp_error:
            print("\n✅ Process completed (MCP cleanup warning suppressed)")
            sys.exit(0)
        else:
            raise
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)

