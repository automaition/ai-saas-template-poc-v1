---
name: backend-api-pattern
description: |
  Crea endpoint FastAPI production-ready per PoC SaaS: async, type-safe con Pydantic v2, 
  gestione file upload, integrazione AI OpenRouter, dependency injection e error handling standardizzato.
  Trigger: "nuovo endpoint", "crea API", "aggiungi route", "endpoint upload", "API AI", 
  "backend crud", "route fastapi", "aggiungi risorsa"
keywords: [api, endpoint, route, crud, fastapi, backend, upload, ai, openrouter, pydantic]
---

## Goal
Generare endpoint FastAPI coerenti con l'architettura PoC: asincroni, con validazione Pydantic, 
gestione centralizzata errori, integrazione facoltativa con OpenRouter e SQLAlchemy, 
pronti per essere esposti via Docker/Coolify.

## Instructions

### 1. Struttura Base Endpoint

Ogni nuova risorsa deve seguire questo pattern:

**File: `app/api/v1/endpoints/nome_risorsa.py`**

```python
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api import deps
from app.services.openrouter import OpenRouterClient, get_openrouter
from app.schemas.nome_risorsa import (
    RisorsaCreate, 
    RisorsaResponse, 
    RisorsaList,
    ProcessResponse
)
from app.models.nome_risorsa import NomeRisorsa
from app.core.database import get_db

router = APIRouter(prefix="/nome-risorsa", tags=["Nome Risorsa"])

@router.get("/", response_model=RisorsaList)
async def list_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Lista paginata risorse"""
    # Implementazione lista
    pass

@router.post("/", response_model=RisorsaResponse, status_code=201)
async def create_item(
    data: RisorsaCreate,
    db: AsyncSession = Depends(get_db)
):
    """Crea nuova risorsa"""
    # Implementazione creazione
    pass

@router.get("/{item_id}", response_model=RisorsaResponse)
async def get_item(
    item_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Recupera singola risorsa"""
    # Implementazione get by id
    pass

@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Elimina risorsa"""
    # Implementazione delete
    pass