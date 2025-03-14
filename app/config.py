import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from .env file (if present)
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "My Microservice")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "changeme")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    
    # (Optional) External API endpoint for demonstration
    EXTERNAL_API_URL: str = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com")

settings = Settings()
