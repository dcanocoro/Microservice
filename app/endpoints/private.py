# app/endpoints/private.py
from fastapi import APIRouter, Depends
from app.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=dict)
def private_endpoint(current_user: User = Depends(get_current_user)):
    """
    Enpoint privado que requiere JWT válido.
    """
    return {"message": f"Hello, {current_user.username}. This is a private endpoint."}
