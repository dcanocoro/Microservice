# app/models/auth.py
from pydantic import BaseModel

class LoginInput(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

