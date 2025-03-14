from fastapi import APIRouter, Depends
from fastapi import HTTPException
import httpx

from app.security import get_current_user, create_access_token, TokenData
from app.config import settings

router = APIRouter()

@router.get("/public")
def public_endpoint():
    """
    Public endpoint that doesn't require authentication.
    """
    return {"message": "Hello from a public endpoint!"}

@router.get("/private")
def private_endpoint(current_user: TokenData = Depends(get_current_user)):
    """
    Private endpoint that requires a valid JWT token.
    """
    return {"message": f"Hello, {current_user.username}. This is a private endpoint."}

@router.get("/external")
def external_api_call():
    """
    Example of making an external API call for demonstration purposes.
    """
    url = f"{settings.EXTERNAL_API_URL}/todos/1"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/token")
def login(username: str, password: str):
    """
    Dummy login endpoint that issues a JWT token.
    In a real-world app, you'd validate the username and password (DB, etc.).
    """
    # For demonstration, assume any username/password is valid
    access_token = create_access_token({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}
