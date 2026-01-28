"""
Health check endpoint for monitoring and Coolify health checks.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings


router = APIRouter(prefix="/health", tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    environment: str
    database: str


@router.get("", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    """
    Health check endpoint.
    Returns status of the application and database connectivity.
    """
    # Check database connectivity
    db_status = "ok"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
    
    return HealthResponse(
        status="ok",
        environment=settings.ENVIRONMENT,
        database=db_status
    )
