from pydantic import BaseModel
from typing import List, Optional


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
