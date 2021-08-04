from pydantic import BaseModel
from typing import List, Optional


class Course(BaseModel):
    id: int
    name: str
    duration: int
    teachers: Optional[List[str]] = []
