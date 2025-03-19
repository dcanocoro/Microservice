from datetime import datetime, timedelta
from typing import Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.config import settings
from app.logging_conf import get_logger 

logger = get_logger()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class TokenData(BaseModel):
    sub: str

def create_access_token(data: dict, expires_delta: Union[int, None] = None):
    """
    Genera un JWT token con expiración.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    logger.info(f"JWT token created for user: {data.get('sub')} (expires in {expires_delta} minutes)")
    
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodifica y verifica un JWT token.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token validation failed: Username not found in token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: username not found",
            )

        logger.info(f"Token successfully validated for user: {username}")
        return TokenData(sub=username)
    
    except jwt.ExpiredSignatureError:
        logger.warning("Token validation failed: Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    except jwt.JWTError:
        logger.warning("Token validation failed: Invalid token signature")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Extracts and returns the current authenticated user.
    """
    user = decode_access_token(token)
    logger.info(f"User authenticated successfully: {user.username}")
    return user


