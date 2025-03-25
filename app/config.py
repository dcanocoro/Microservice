# app/config.py
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "My Microservice")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Control para desactivar TODA la seguridad en local
    ARCHITECTURE_HANDLERS_SECURITY_ENABLED: bool = os.getenv("ARCHITECTURE_HANDLERS_SECURITY_ENABLED", "true").lower() == "true"

    # JWT/JWKS settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "changeme")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
    
    # Opcional: Si usas un servicio PKM para JWKS
    PKM_JWKS_URL: str = os.getenv("PKM_JWKS_URL", "http://pkm-service/jwks")
    JWKS_CACHE_TIMEOUT: int = int(os.getenv("JWKS_CACHE_TIMEOUT", "3600"))

    # Ejemplo: configuración de AdminLDAP para autorización
    ADMINLDAP_URL: str = os.getenv("ADMINLDAP_URL", "http://ldap-service/api/checkPermission")
    ADMINLDAP_CLIENT_ID: str = os.getenv("ADMINLDAP_CLIENT_ID", "myclientid")
    ADMINLDAP_CLIENT_SECRET: str = os.getenv("ADMINLDAP_CLIENT_SECRET", "myclientsecret")

    # Resto de configuraciones...
    EXTERNAL_API_URL: str = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com")

settings = Settings()


