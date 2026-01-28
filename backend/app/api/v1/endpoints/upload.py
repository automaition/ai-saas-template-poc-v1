"""
File upload endpoint with validation.
"""
import os
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.config import settings


router = APIRouter(prefix="/upload", tags=["Upload"])


class UploadResponse(BaseModel):
    """Upload response schema."""
    filename: str
    content_type: str
    size: int
    message: str


@router.post("/", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
) -> UploadResponse:
    """
    Upload a file with validation.
    
    - Validates file size (max 10MB default)
    - Validates MIME type against allowed list
    - Returns file metadata
    """
    # Validate content type
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{file.content_type}' not allowed. Allowed types: {settings.ALLOWED_MIME_TYPES}"
        )
    
    # Read file content to check size
    content = await file.read()
    file_size = len(content)
    
    # Validate file size
    if file_size > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size {file_size} bytes exceeds maximum {settings.max_upload_size_bytes} bytes"
        )
    
    # Reset file position for potential future reads
    await file.seek(0)
    
    # Here you would typically:
    # 1. Save to disk or cloud storage
    # 2. Create database record
    # 3. Queue for processing
    
    # For template: just return metadata
    return UploadResponse(
        filename=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
        size=file_size,
        message="File uploaded successfully. Implement storage logic as needed."
    )
