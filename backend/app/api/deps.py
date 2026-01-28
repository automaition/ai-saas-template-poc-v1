"""
API dependencies for dependency injection.
"""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db as _get_db
from app.core.openrouter import OpenRouterClient, get_openrouter as _get_openrouter


# Type aliases for cleaner dependency injection
DbSession = Annotated[AsyncSession, Depends(_get_db)]
AIClient = Annotated[OpenRouterClient, Depends(_get_openrouter)]


# Re-export for direct import
get_db = _get_db
get_openrouter = _get_openrouter
