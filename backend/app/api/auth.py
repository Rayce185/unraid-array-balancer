"""Authentication API endpoints."""

from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt
from pydantic import BaseModel

from app.services.config import settings

router = APIRouter()
security = HTTPBasic()


class Token(BaseModel):
    """JWT token response."""
    
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class LoginRequest(BaseModel):
    """Login request body."""
    
    username: str
    password: str


def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify a password against the stored value."""
    # For now, simple comparison. In production, use hashed passwords.
    return plain_password == stored_password


def create_access_token(username: str) -> tuple[str, datetime]:
    """Create a JWT access token."""
    expires = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode = {
        "sub": username,
        "exp": expires,
    }
    
    token = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return token, expires


@router.post("/login", response_model=Token)
async def login(request: LoginRequest) -> Token:
    """
    Authenticate and receive a JWT token.
    
    Default credentials:
    - Username: admin
    - Password: arraybalancer
    """
    if not settings.auth_enabled:
        # Auth disabled, return a token anyway
        token, expires = create_access_token(request.username)
        return Token(access_token=token, expires_at=expires)
    
    if request.username != settings.auth_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    if not verify_password(request.password, settings.auth_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    
    token, expires = create_access_token(request.username)
    return Token(access_token=token, expires_at=expires)


@router.get("/me")
async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> dict:
    """Get current authenticated user info."""
    return {
        "username": credentials.username,
        "auth_enabled": settings.auth_enabled,
        "using_default_password": settings.auth_password == "arraybalancer",
    }


@router.get("/status")
async def auth_status() -> dict:
    """Get authentication status and configuration."""
    return {
        "auth_enabled": settings.auth_enabled,
        "using_default_credentials": (
            settings.auth_username == "admin" and 
            settings.auth_password == "arraybalancer"
        ),
    }
