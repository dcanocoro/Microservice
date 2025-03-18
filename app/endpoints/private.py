# app/endpoints/private.py
from fastapi import APIRouter, Depends
from app.security.jwt import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=dict)
def private_endpoint(current_user: User = Depends(get_current_user)):
    """
    Private endpoint that requires valid JWT.
    """
    return {"message": f"Hello, {current_user.username}. This is a private endpoint."}
