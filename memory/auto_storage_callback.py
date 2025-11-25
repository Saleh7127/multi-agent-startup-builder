import json
from google.adk.agents.callback_context import CallbackContext
from .memory_config import memory_service, session_service
from .agent_mapping import get_agent_name_from_output_key

APP_NAME = "startup-builder"


async def auto_store_agent_responses(callback_context: CallbackContext):
    """
    Automatically store session to memory after each agent completes.
    Uses callback_context._invocation_context.memory_service.add_session_to_memory(session)
    """
    try:
        invocation_context = callback_context._invocation_context
        
        if not invocation_context:
            print("⚠️  No invocation_context in callback")
            return
        
        # Use the global memory_service (Sqlite) for persistence
        # The context's memory_service might be InMemoryMemoryService when running as a Tool
        
        from .memory_config import memory_service as global_memory_service
        memory_svc = global_memory_service
        
        # print(f"🔍 Memory Service Type: {type(memory_svc)}")
        session = invocation_context.session
        
        if not memory_svc:
            print("⚠️  No global memory_service available")
            return
        
        if not session:
            print("⚠️  No session in invocation_context")
            return
        
        await memory_svc.add_session_to_memory(session)
        
    except Exception as e:
        print(f"⚠️  Error in auto_store_agent_responses: {e}")
        import traceback
        traceback.print_exc()

