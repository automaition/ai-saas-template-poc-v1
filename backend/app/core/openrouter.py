"""
OpenRouter AI client with async support, retry logic, and SSE streaming.
"""
import json
from typing import Any, AsyncGenerator, Dict, Optional

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.core.config import settings


class OpenRouterClient:
    """Async client for OpenRouter API with retry and streaming support."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.model = model or settings.OPENROUTER_MODEL
        self.base_url = base_url or settings.OPENROUTER_BASE_URL
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is required")
        
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.SITE_URL,
            "X-Title": settings.SITE_NAME,
            "Content-Type": "application/json"
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException))
    )
    async def complete(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send completion request with retry logic.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Override default model
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens in response
            response_format: Optional format spec (e.g., {"type": "json_object"})
        
        Returns:
            Full API response as dict
        """
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs
        }
        
        if response_format:
            payload["response_format"] = response_format
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self._headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
    
    async def complete_stream(
        self,
        messages: list[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Stream completion response as SSE events.
        
        Yields:
            Content chunks as strings
        """
        payload = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            **kwargs
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=self._headers,
                json=payload
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
    
    async def get_content(
        self,
        messages: list[Dict[str, str]],
        **kwargs
    ) -> str:
        """Helper to get just the content string from completion."""
        response = await self.complete(messages, **kwargs)
        return response["choices"][0]["message"]["content"]


# Dependency injection
def get_openrouter() -> OpenRouterClient:
    """Get OpenRouter client instance for dependency injection."""
    return OpenRouterClient()
