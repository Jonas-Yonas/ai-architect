from pydantic import BaseModel
from typing import List, Optional, Dict


# This is the "Contract" between us and the AI.
# We tell Gemini: "You MUST respond in THIS exact JSON format."
class ArchitecturePlan(BaseModel):
    project_type: str  # e.g., "SaaS", "E-commerce"
    primary_language: str  # e.g., "Python", "TypeScript"

    # Nested objects for the stack
    frontend: str
    backend: str
    database: str
    caching: Optional[str]

    # Actionable advice
    folder_structure_hint: str
    first_phase_tasks: List[str]  # List of 3 things to build first


class Conversation(BaseModel):
    messages: List[
        Dict[str, str]
    ] = []  # Each message: {"role": "user" or "assistant", "content": "message text" ...}
