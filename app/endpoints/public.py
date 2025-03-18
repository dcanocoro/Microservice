# app/endpoints/public.py
from fastapi import APIRouter
from app.models.user import PublicUser  # Example: a Pydantic model

router = APIRouter()

@router.get("/", response_model=dict)
def root_public_endpoint():
    """
    Public endpoint that doesn't require authentication.
    E.g., might return a landing message or service info.
    """
    return {"message": "Welcome to the public endpoint!"}

@router.get("/info", response_model=PublicUser)
def get_public_user_info():
    """
    Demonstrates returning a typed Pydantic model.
    """
    return PublicUser(username="guest", email="guest@example.com")
