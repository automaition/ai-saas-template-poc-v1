"""
API v1 router - aggregates all v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import health, upload


router = APIRouter(prefix="/api/v1")

# Include all endpoint routers
router.include_router(health.router)
router.include_router(upload.router)
