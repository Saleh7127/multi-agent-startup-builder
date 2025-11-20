TECHNICAL_ARCHITECT_PROMPT = """
Design technical architecture. Return JSON only:

{
  "technical_architecture": {
    "platform": "Platform/stack",
    "frontend": "Frontend tech",
    "backend": "Backend tech",
    "database": "Database tech",
    "key_components": ["Component1"],
    "integrations": ["Integration1"],
    "infrastructure": "Infrastructure"
  },
  "development_roadmap": {
    "timeline": "Timeline",
    "milestones": [{"milestone": "Name", "description": "Desc", "estimated_time": "Time"}],
    "resources_needed": {"team": ["Role1"], "tools": ["Tool1"], "services": ["Service1"]}
  },
  "technical_considerations": {
    "scalability": "Scalability",
    "security": "Security",
    "performance": "Performance",
    "maintenance": "Maintenance"
  }
}
"""

