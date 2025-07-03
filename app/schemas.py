from pydantic import BaseModel
from typing import Optional

class CurriculumRequest(BaseModel):
    goal: str
    known_skills: Optional[str] = None