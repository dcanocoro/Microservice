# app/endpoints/external.py
from fastapi import APIRouter, HTTPException
import httpx
from app.config import settings
from app.models.external import Todo  # Example Pydantic model for external data

router = APIRouter()

@router.get("/todo", response_model=Todo)
def fetch_todo_item():
    """
    Example of making an external API call and returning structured data.
    """
    url = f"{settings.EXTERNAL_API_URL}/todos/1"
    try:
        response = httpx.get(url, timeout=10)  # set a timeout
        response.raise_for_status()
        data = response.json()
        return Todo(**data)  # Validate data with Pydantic model
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=str(e))
    