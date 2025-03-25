# app/security/headers.py
from fastapi import Depends, HTTPException, status
from fastapi.params import Header
from app.config import settings

def validate_headers(
    application_id: str = Header(None, alias="Application-Id"),
    channel: str = Header(None, alias="Channelxx"),
    token_header: str = Header(None, alias="Tokenxx")
) -> dict:
    """
    Dependencia que valida las cabeceras requeridas.
    Retorna un dict con cabeceras limpias que se pueden
    propagar a la siguiente fase de seguridad.
    """

    if not settings.ARCHITECTURE_HANDLERS_SECURITY_ENABLED:
        # Si está desactivada la seguridad, no validamos nada
        return {}

    # Ejemplo de validación: application_id y channel son obligatorios
    if not application_id or not channel:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required headers: 'Application-Id' or 'Channelxx'"
        )
    
    # Tokenxx podría considerarse opcional según tu caso; aquí lo marcamos
    # como obligatorio para la fase de autenticación
    if not token_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Tokenxx header"
        )
    
    return {
        "Application-Id": application_id,
        "Channelxx": channel,
        "Tokenxx": token_header
    }
