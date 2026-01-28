---
name: database-layer
description: |
  Configura SQLAlchemy 2.0 async per SQLite. Pattern: UUID, timestamp auto, 
  campi JSON flessibili, soft delete. Modelli base per requisiti variabili.
  Trigger: "modello database", "entità sqlalchemy", "tabella", "schema db", "migration"
keywords: [database, sqlalchemy, model, entity, sqlite, orm, async, alembic]
---

## Goal
Creare modelli SQLAlchemy 2.0 async robusti con SQLite, supporto JSON per dati variabili del cliente, e pattern CRUD standardizzati.

## Instructions

1. **Setup Connessione**:
   - SQLAlchemy async con `create_async_engine("sqlite+aiosqlite:///...")`
   - `AsyncSessionLocal` con `expire_on_commit=False`
   - Dependency FastAPI `get_db()` che yielda `AsyncSession`
   - Inizializzazione tabelle: `Base.metadata.create_all()` in dev (opzionale Alembic)

2. **Modello Base**:
   - Tutti i modelli ereditano da `Base` (declarative_base)
   - Campi obbligatori: `id` (UUID string), `created_at`, `updated_at` (DateTime UTC), `is_active` (bool, soft delete)
   - Campo opzionale `metadata_json: Mapped[dict | None]` (JSON type) solo se struttura dati variabile
   - Mai usare Integer auto-increment per ID (solo UUID)

3. **Nuovo Modello**:
   - File: `app/models/nome.py`
   - Type hints: `Mapped[type] = mapped_column(...)`
   - Campi specifici tipizzati se struttura nota, JSON solo per dati arbitrari del cliente
   - Index su campi frequentemente filtrati (status, user_id, ecc.)
   - Relationships con `selectinload` per evitare N+1 (se necessario)

4. **CRUD Pattern**:
   - Service layer separato da router: `app/services/nome_service.py`
   - Metodi: `create()`, `get()`, `get_multi()` (con skip/limit/filtri), `update()`, `delete()` (soft)
   - Query con `select()`, `where()`, `offset()`, `limit()`, `order_by(desc())`
   - Commit esplicito: `await db.commit()` + `await db.refresh(obj)`

5. **Alembic** (opzionale per PoC):
   - Comandi: `alembic revision --autogenerate -m "msg"`, `alembic upgrade head`
   - Configurazione env.py con `target_metadata = Base.metadata`
   - Per PoC rapido: skip Alembic, usa `create_all()`

## Constraints

- Solo SQLite async (`aiosqlite`)
- Solo SQLAlchemy 2.0 style (`select()`, `Mapped[]`, mai `query.get()`)
- Solo AsyncSession (mai sessione sincrona)
- UUID sempre stringa (no Integer)
- Soft delete default (flag `is_active`, mai hard delete diretto)
- JSON solo per dati variabili (se struttura fissa, usare colonne tipizzate)
- NO raw SQL injection (usare ORM/parametrizzato)
- NO lazy loading senza eager load (evita N+1)

## Examples

### Esempio utilizzo per Antigravity
Utente: "Crea modello Document per salvare PDF processati con AI"

Azioni:
1. Modello `Document` con: id UUID, filename (str), content_type (str), status (str, indexed), extracted_data (JSON nullable), timestamps
2. Service `DocumentService` con metodi CRUD async
3. Schema Pydantic correlato (vedi skill backend-api-pattern)
4. Integrazione in router con `Depends(get_db)`