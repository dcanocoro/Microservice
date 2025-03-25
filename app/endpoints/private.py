# app/endpoints/private.py
from fastapi import APIRouter, Depends
from app.security.autenticacion import authenticate_token

router = APIRouter()

@router.get("/", response_model=dict)
def private_endpoint(
    token_payload: dict = Depends(authenticate_token)
):
    """
    Privado: requiere cabeceras correctas y JWT válido.
    """
    username = token_payload.get("sub", "unknown_user")
    return {"message": f"Hola, {username}. Este es un endpoint privado."}

