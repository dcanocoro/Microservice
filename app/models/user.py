# app/models/user.py
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
    # Add more user-related fields if needed

class PublicUser(BaseModel):
    username: str
    email: Optional[str] = None
