# app/security/authentication.py
import httpx
import time
import jwt
from fastapi import Depends, HTTPException, status
from typing import Optional, Dict, Any
from app.config import settings
from app.security.cabeceras import validate_headers
from app.utilities.logging_conf import get_logger

logger = get_logger()

# Simple caché en memoria
JWKS_CACHE: Dict[str, Any] = {}
JWKS_EXPIRES_AT: float = 0.0

def get_jwks() -> dict:
    """
    Obtiene las claves públicas JWKS desde PKM, con caché.
    """
    global JWKS_CACHE, JWKS_EXPIRES_AT
    current_time = time.time()

    if current_time < JWKS_EXPIRES_AT and JWKS_CACHE:
        return JWKS_CACHE
    
    # Caso: caché vencida o no inicializada
    try:
        response = httpx.get(settings.PKM_JWKS_URL, timeout=10)
        response.raise_for_status()
        JWKS_CACHE = response.json()
        JWKS_EXPIRES_AT = current_time + settings.JWKS_CACHE_TIMEOUT
        logger.info("JWKS cache refreshed successfully.")
        return JWKS_CACHE
    except httpx.HTTPError as exc:
        logger.error(f"Error fetching JWKS: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch JWKS"
        )


def decode_access_token(token: str) -> dict:
    """
    Decodifica el JWT. Puede usarse la JWKS si fuese RS256, etc.
    """
    if not settings.ARCHITECTURE_HANDLERS_SECURITY_ENABLED:
        # Si la seguridad está desactivada, devolvemos un payload mínimo
        return {"sub": "local_user"}
    
    try:
        # Ejemplo: si usas HS256 local:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def authenticate_token(headers: dict = Depends(validate_headers)) -> dict:
    """
    Segunda fase de la cadena: autenticar el usuario via JWT 
    (tras haber validado cabeceras).
    """
    token = headers.get("Tokenxx")
    # decode_access_token lanzará excepción en caso de token inválido
    payload = decode_access_token(token)
    return payload
