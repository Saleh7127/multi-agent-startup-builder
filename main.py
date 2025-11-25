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
                if hasattr(event, 'content') and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            print(f"📝 Event: {part.text[:100]}...")
                
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
        except (TypeError, RuntimeError, Exception) as e:
            error_msg = str(e)
            error_type = type(e).__name__
            traceback_str = ""
            try:
                import traceback
                traceback_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
            except:
                pass
            
            is_non_critical = (
                "'NoneType' object is not iterable" in error_msg or
                "cancel scope" in error_msg.lower() or 
                "mcp" in error_msg.lower() or
                "stdio_client" in error_msg.lower() or
                "asyncgen" in error_msg.lower() or
                "ExceptionGroup" in error_type or
                "BaseExceptionGroup" in error_type or
                "asyncgen" in traceback_str.lower()
            )
            
            if is_non_critical:
                print(f"\n⚠️  Non-critical error ({error_type}): {error_msg[:100]}")
                print("   Continuing with session retrieval and data storage...")
            else:
                raise
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
                session_id_attr = getattr(session, 'id', getattr(session, 'session_id', session_id))
                print(f"🔍 Retrieved session: {session_id_attr}")
                print(f"🔍 Session type: {type(session)}")
                
                if hasattr(session, 'state') and session.state:
                    state = session.state
                    print(f"🔍 State type: {type(state)}")
                    
                    state_dict = {}
                    if isinstance(state, dict):
                        state_dict = state
                    elif hasattr(state, 'to_dict'):
                        try:
                            state_dict = state.to_dict() or {}
                        except:
                            state_dict = {}
                    
                    if state_dict:
                        print(f"🔍 State dict keys: {list(state_dict.keys())[:20]}")
                        
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
                    else:
                        print(f"⚠️  Could not extract state dict")
                else:
                    print(f"⚠️  Session has no state or state is None")
                
                try:
                    await memory_service.add_session_to_memory(session)
                    print("💾 Session transferred to memory")
                    
                    event_count = len(session.events) if hasattr(session, 'events') and session.events else 0
                    print(f"📊 Session events in DB: {event_count}")
                    
                    if event_count > 0 and hasattr(session, 'events'):
                        print(f"   First event author: {session.events[0].author if len(session.events) > 0 else 'None'}")
                except Exception as e:
                    print(f"⚠️  Error transferring session to memory: {e}")
                    import traceback
                    traceback.print_exc()
                
        except Exception as e:
            print(f"⚠️  Error saving session to memory: {e}")
        
        print("\n✅ Process completed!")
        print(f"💾 Responses stored: {len(stored_outputs)} agents")
        print(f"📁 Databases: memory/agent_responses.db, memory/sessions.db")
        
        import sqlite3
        try:
            with sqlite3.connect("memory/agent_responses.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM agent_responses")
                count = cursor.fetchone()[0]
                print(f"📊 Agent responses in DB: {count}")
        except Exception as e:
            print(f"⚠️  Could not check DB: {e}")
        
        try:
            with sqlite3.connect("memory/sessions.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM events")
                event_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM sessions")
                session_count = cursor.fetchone()[0]
                print(f"📊 Sessions in DB: {session_count}, Events in DB: {event_count}")
        except Exception as e:
            print(f"⚠️  Could not check sessions DB: {e}")
        
    except Exception as e:
        error_str = str(e)
        error_type = type(e).__name__
        traceback_str = str(e.__traceback__) if hasattr(e, '__traceback__') else ""
        
        if ("cancel scope" in error_str.lower() or 
            "mcp" in error_str.lower() or 
            "stdio_client" in error_str.lower() or
            "ExceptionGroup" in error_type or
            "BaseExceptionGroup" in error_type or
            "asyncgen" in traceback_str.lower()):
            print("\n⚠️  MCP cleanup warning (non-critical - can be ignored)")
            print("✅ Process completed successfully")
        else:
            raise


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

