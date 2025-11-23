import os
from pathlib import Path
from google.adk.runners import InMemorySessionService
from .sqlite_memory_service import SqliteMemoryService

project_root = Path(__file__).parent.parent

session_service = InMemorySessionService()
memory_service = SqliteMemoryService()
