import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from google.adk.runners import BaseMemoryService
from memory.agent_mapping import get_agent_name_from_output_key

project_root = Path(__file__).parent.parent
DB_PATH = project_root / "memory" / "agent_responses.db"


class SqliteMemoryService(BaseMemoryService):
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    async def add_session_to_memory(self, session):
        """
        Transfer session data to memory storage.
        Based on notebook pattern: extracts agent responses from session state.
        Also stores session events for cross-session retrieval.
        """
        try:
            if not session:
                print("⚠️  No session provided to add_session_to_memory")
                return
            
            app_name = 'startup-builder'
            
            session_id = getattr(session, 'id', None) or getattr(session, 'session_id', None)
            user_id = getattr(session, 'user_id', None)
            
            if not session_id or not user_id:
                print(f"⚠️  Missing session_id or user_id. Session attrs: {[a for a in dir(session) if not a.startswith('__')][:20]}")
                return
            
            print(f"🔍 Processing session: {session_id}, user: {user_id}")
            
            state = getattr(session, 'state', None)
            if not state:
                print(f"⚠️  Session has no state: {session_id}")
                return
            
            stored_count = 0
            
            state_dict = {}
            if isinstance(state, dict):
                state_dict = state
            elif hasattr(state, 'to_dict'):
                try:
                    state_dict = state.to_dict() or {}
                except:
                    state_dict = {}
            else:
                print(f"⚠️  Session state is not a dict and has no to_dict method. State type: {type(state)}")
                return
            
            if state_dict:
                all_keys = list(state_dict.keys())
                result_keys = [k for k in all_keys if k.endswith('_result')]
                print(f"🔍 State dict has {len(state_dict)} keys")
                print(f"🔍 All keys (first 30): {all_keys[:30]}")
                print(f"🔍 Result keys found: {result_keys}")
            else:
                print(f"⚠️  State dict is empty")
                return
            
            for output_key, value in state_dict.items():
                if output_key.endswith('_result') and value:
                    agent_name = get_agent_name_from_output_key(output_key)
                    try:
                        if isinstance(value, str):
                            response_str = value
                        elif isinstance(value, dict):
                            import json
                            response_str = json.dumps(value, ensure_ascii=False)
                        else:
                            response_str = str(value)
                        
                        if response_str and response_str.strip():
                            self.store_agent_response(
                                app_name=app_name,
                                user_id=user_id,
                                session_id=session_id,
                                agent_name=agent_name,
                                response_json=response_str,
                            )
                            stored_count += 1
                            print(f"💾 Stored from state: {agent_name}")
                    except Exception as e:
                        print(f"⚠️  Error storing {agent_name}: {e}")
            
            events = getattr(session, 'events', None)
            if events:
                print(f"🔍 Processing {len(events)} session events...")
                for event in events:
                    author = getattr(event, 'author', None)
                    content = getattr(event, 'content', None)
                    
                    if author and content and hasattr(content, 'parts') and content.parts:
                        for part in content.parts:
                            text = getattr(part, 'text', None)
                            if text and author.endswith('_agent'):
                                agent_name = author
                                try:
                                    if text and text.strip():
                                        self.store_agent_response(
                                            app_name=app_name,
                                            user_id=user_id,
                                            session_id=session_id,
                                            agent_name=agent_name,
                                            response_json=text,
                                        )
                                        stored_count += 1
                                        print(f"💾 Stored from event: {agent_name}")
                                except Exception as e:
                                    print(f"⚠️  Error storing event {agent_name}: {e}")
            
            if stored_count > 0:
                print(f"✅ Stored {stored_count} agent responses to memory")
            else:
                print(f"⚠️  No agent responses found. State keys: {list(state_dict.keys())}, Events: {len(events) if events else 0}")
        except Exception as e:
            print(f"⚠️  Error adding session to memory: {e}")
            import traceback
            traceback.print_exc()
    
    async def search_memory(self, query: str, user_id: str = None, limit: int = 10):
        """
        Search memory for relevant responses.
        For now, simple keyword matching in response_json.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            conditions = ["response_json LIKE ?"]
            params = [f"%{query}%"]
            
            if user_id:
                conditions.append("user_id = ?")
                params.append(user_id)
            
            where_clause = " AND ".join(conditions)
            params.append(limit)
            
            cursor.execute(f"""
                SELECT app_name, user_id, session_id, agent_name, response_json, created_at
                FROM agent_responses
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT ?
            """, params)
            
            results = cursor.fetchall()
            conn.close()
            
            from google.adk.memory import memory_entry
            from google.adk.types import Content, Part
            import json
            
            memories = []
            for r in results:
                try:
                    content = Content(
                        parts=[Part(text=r[4])],
                        role="model"
                    )
                    memory = memory_entry.MemoryEntry(
                        author=r[3],
                        content=content,
                    )
                    memories.append(memory)
                except Exception as e:
                    pass
            
            from google.adk.memory import SearchMemoryResponse
            return SearchMemoryResponse(memories=memories)
        except Exception as e:
            from google.adk.memory import SearchMemoryResponse
            return SearchMemoryResponse(memories=[])

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT NOT NULL,
                user_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                response_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(app_name, user_id, session_id, agent_name)
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session 
            ON agent_responses(app_name, user_id, session_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_agent 
            ON agent_responses(agent_name)
        """)
        conn.commit()
        conn.close()

    def store_agent_response(
        self,
        app_name: str,
        user_id: str,
        session_id: str,
        agent_name: str,
        response_json: str,
    ):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO agent_responses 
            (app_name, user_id, session_id, agent_name, response_json)
            VALUES (?, ?, ?, ?, ?)
        """, (app_name, user_id, session_id, agent_name, response_json))
        conn.commit()
        conn.close()

    def get_agent_response(
        self,
        app_name: str,
        user_id: str,
        session_id: str,
        agent_name: str,
    ) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT response_json FROM agent_responses
            WHERE app_name = ? AND user_id = ? AND session_id = ? AND agent_name = ?
        """, (app_name, user_id, session_id, agent_name))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_session_responses(
        self,
        app_name: str,
        user_id: str,
        session_id: str,
    ) -> Dict[str, str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT agent_name, response_json FROM agent_responses
            WHERE app_name = ? AND user_id = ? AND session_id = ?
        """, (app_name, user_id, session_id))
        results = cursor.fetchall()
        conn.close()
        return {agent_name: response_json for agent_name, response_json in results}

    def search_responses(
        self,
        agent_name: Optional[str] = None,
        app_name: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        conditions = []
        params = []
        
        if agent_name:
            conditions.append("agent_name = ?")
            params.append(agent_name)
        if app_name:
            conditions.append("app_name = ?")
            params.append(app_name)
        if user_id:
            conditions.append("user_id = ?")
            params.append(user_id)
        
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        params.append(limit)
        
        cursor.execute(f"""
            SELECT app_name, user_id, session_id, agent_name, response_json, created_at
            FROM agent_responses
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ?
        """, params)
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "app_name": r[0],
                "user_id": r[1],
                "session_id": r[2],
                "agent_name": r[3],
                "response_json": r[4],
                "created_at": r[5],
            }
            for r in results
        ]

