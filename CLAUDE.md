# FloraVoice FastAPI — Project Guide

## Project Overview

Flower e-commerce backend. FastAPI + async SQLAlchemy + PostgreSQL. AI voice/chat agents place orders on behalf of customers.

## Tech Stack

- **Python** 3.14.3 (see `.python-version`)
- **FastAPI** >= 0.135.1
- **SQLAlchemy** >= 2.0.48 (async)
- **asyncpg** >= 0.31.0
- **PyJWT** >= 2.12.1 + **bcrypt** >= 5.0.0
- **UV** (package manager)
- **Ruff** (linter)

## Running the Project

```bash
# Install dependencies
uv sync

# Copy env and fill in values
cp .env.example .env

# Run migrations (manual SQL execution)
psql -h localhost -U <user> -d <db> -f migrations/sql/001_initial_migration.sql
psql -h localhost -U <user> -d <db> -f migrations/sql/002_add_address_to_users.sql
psql -h localhost -U <user> -d <db> -f migrations/sql/003_add_orders.sql

# Start dev server
fastapi dev app/main.py
```

Docs at `http://localhost:8000/docs`.

## Architecture

Strict layered architecture — never skip layers:

```
Routers → Services → Repositories → Models
```

| Layer | Location | Responsibility |
|-------|----------|----------------|
| Routers | `app/routers/` | HTTP endpoints, catch exceptions, return HTTPException |
| Services | `app/services/` | Business logic, orchestrate repositories |
| Repositories | `app/repositories/` | All DB queries, static methods, AsyncSession |
| Models | `app/models/` | SQLAlchemy ORM definitions |
| Schemas | `app/schemas/` | Pydantic validation — Create/Update/Response per entity |
| Exceptions | `app/exceptions/` | Custom exceptions per domain |
| Dependencies | `app/dependancies/` | FastAPI deps (auth, db session) |
| Migrations | `migrations/sql/` | Sequential numbered raw SQL files |

## Key Conventions

- **UUID PKs** everywhere (`uuid4`, `as_uuid=True`)
- **All repository methods are static**
- **Async** all the way — `AsyncSession`, `await db.execute()`
- **ORM → Schema** via `Model.model_validate(orm_obj)`
- **UUID serialization** in Response schemas uses `@field_serializer`
- **Relationships** use `lazy="selectin"` for async safety (avoids `MissingGreenlet`)
- **Explicit `selectinload()`** in repository queries when relationships are needed
- **Update semantics (PUT)**: all fields required, no `Optional` with `None` defaults
- **Migrations**: never add `DEFAULT` values to `NOT NULL` columns unless explicitly needed

## Authentication

Two separate account types sharing the same JWT mechanism:

- `get_current_user` — validates token against `users` table
- `get_current_admin` — validates token against `admins` table
- Unused auth dependencies use `_` as the variable name: `_: AdminModel = Depends(get_current_admin)`
- Access token: 5 days | Refresh token: 30 days | Algorithm: HS256

## Error Handling Pattern

Services raise custom exceptions. Routers catch and convert:

```python
# service
raise FlowerNotFound(f"Flower '{id}' not found")

# router
except FlowerNotFound as e:
    raise HTTPException(status_code=404, detail=str(e))
```

## Adding a New Resource

1. `migrations/sql/00N_<name>.sql` — SQL migration
2. `app/models/<name>.py` — SQLAlchemy model
3. `app/exceptions/<name>_exceptions.py` — custom exceptions
4. `app/schemas/<name>/<name>_schemas.py` + `__init__.py`
5. `app/repositories/<name>_repository.py` — static async methods
6. `app/services/<name>_service.py` — business logic functions
7. `app/routers/<name>_router.py` — endpoints
8. `app/routers/main_router.py` — add import + `include_router`

## Environment Variables

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=
DB_PASSWORD=
DB_NAME=
JWT=
```
