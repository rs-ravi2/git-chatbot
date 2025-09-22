from fastapi import HTTPException, status, Depends, Header
from src.config.settings import settings
import logging
import secrets
from typing import Optional

logger = logging.getLogger(__name__)

def verify_api_key(authorization: Optional[str] = Header(None)) -> str:
    """
    Verify API key using simple token in Authorization header.
    Expected format: Authorization: <api_key>
    """
    if not settings.API_KEY:
        logger.error("API_KEY not configured in environment variables")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication not configured"
        )
    
    if not authorization:
        logger.warning("Missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    
    # Use constant-time comparison to prevent timing attacks
    provided_key = authorization.strip()
    expected_key = settings.API_KEY
    
    if not secrets.compare_digest(provided_key, expected_key):
        logger.warning("No valid API key provided")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No valid API key provided"
        )
    
    logger.info("Authentication successful")
    return provided_key