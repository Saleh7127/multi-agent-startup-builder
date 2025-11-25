import os
from pathlib import Path
from google.adk.sessions import DatabaseSessionService
from .sqlite_memory_service import SqliteMemoryService

project_root = Path(__file__).parent.parent

db_url = f"sqlite:///{project_root / 'memory' / 'sessions.db'}"
session_service = DatabaseSessionService(db_url=db_url)
memory_service = SqliteMemoryService()
