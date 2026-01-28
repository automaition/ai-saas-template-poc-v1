"""
Application configuration using Pydantic Settings.
Environment variables are loaded from .env file or system environment.
"""
import json
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = "Agent PoC Template"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # OpenRouter AI Configuration
    OPENROUTER_API_KEY: str = Field(default="")
    OPENROUTER_MODEL: str = Field(default="openai/gpt-4o-mini")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1")
    
    # Site URL for OpenRouter headers
    SITE_URL: str = Field(default="http://localhost:8000")
    SITE_NAME: str = Field(default="Agent PoC Template")
    
    # Database
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./data/app.db")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000", "http://localhost:80", "http://localhost"]
    )
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_MIME_TYPES: List[str] = Field(
        default=["application/pdf", "image/png", "image/jpeg", "text/plain"]
    )
    
    @property
    def max_upload_size_bytes(self) -> int:
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
