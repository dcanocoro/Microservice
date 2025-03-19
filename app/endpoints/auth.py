# app/endpoints/auth.py
from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
from app.security import create_access_token
from app.models.auth import LoginInput, LoginResponse

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(data: LoginInput):
    """
    Dummy login endpoint.
    Validate username/password (e.g., DB check) before issuing token.
    """
    # In a real app, you'd verify user credentials here
    if not data.username or not data.password:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create the token
    access_token = create_access_token({"sub": data.username})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer"
    )
