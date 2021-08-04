from pydantic import BaseModel
from typing import List


class Course(BaseModel):
    name: str
    duration: str
    teachers: List[str]


class Student(BaseModel):
    name: str
    course_id: int


class AuthDetails(BaseModel):
    username: str
    password: str
