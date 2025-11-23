import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from google.adk.runners import BaseMemoryService

project_root = Path(__file__).parent.parent
DB_PATH = project_root / "memory" / "agent_responses.db"


class SqliteMemoryService(BaseMemoryService):
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def add_session_to_memory(self, session_id: str, user_id: str):
        pass
    
    def search_memory(self, query: str, user_id: str = None, limit: int = 10):
        return []

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

