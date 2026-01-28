"""
SQLAlchemy 2.0 declarative base with common mixins for all models.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import DateTime, String, Boolean, JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def generate_uuid() -> str:
    """Generate UUID string for primary keys."""
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all SQLAlchemy models with async support."""
    
    type_annotation_map = {
        dict[str, Any]: JSON
    }


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False
    )


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


class UUIDMixin:
    """Mixin for UUID primary key."""
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid
    )


class BaseModel(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    Abstract base model with UUID, timestamps, and soft delete.
    Use as base class for all domain models.
    """
    
    __abstract__ = True
    
    # Optional JSON field for flexible metadata
    metadata_json: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True
    )
