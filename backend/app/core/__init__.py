"""Core module - configuration, database, and AI client."""
from app.core.config import settings, get_settings
from app.core.openrouter import OpenRouterClient, get_openrouter

__all__ = ["settings", "get_settings", "OpenRouterClient", "get_openrouter"]
