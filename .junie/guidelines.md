# Tibiantis Bot Scraper - Project Guidelines

## Project Overview

A FastAPI-based web scraper and monitoring bot for [tibiantis.online](https://tibiantis.online) character data, with Discord notification capabilities.

## Core Features

### 1. Character Scraping
- Scrape character data from tibiantis.online character pages
- Store character information (name, sex, vocation, level, world, residence, house, guild, last_login, account_status) in PostgreSQL
- Periodic or on-demand scraping support

### 2. Blacklist Management
- Add characters to a blacklist for online-status monitoring
- Full CRUD operations for blacklisted characters:
  - **Create**: Add a character to the blacklist
  - **Read**: Get all blacklisted characters or a specific one
  - **Update**: Modify blacklist entry (e.g., update monitoring settings)
  - **Delete**: Remove a character from the blacklist

### 3. Bedmage Timers & Discord Notifications
- Track "bedmage" timers for specific players
- After X minutes since a player's last login, trigger a Discord bot notification
- Configurable timer duration per player
- Discord webhook/bot integration for real-time alerts

## Tech Stack

- **Language**: Python 3.13
- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.x
- **Migrations**: Alembic (autogenerate from models)
- **Database**: PostgreSQL 17.5 (Dockerized)
- **Settings**: pydantic-settings (`.env` file)
- **Containerization**: Docker + Docker Compose
- **Package Manager**: Poetry (poetry-core 2.x)

## Project Structure

```
tibiantis-bot-scraper/
├── app/
│   ├── core/
│   │   ├── config.py          # Settings (pydantic-settings, .env)
│   │   └── database.py        # SQLAlchemy engine, session, Base
│   ├── models/
│   │   ├── __init__.py        # Import all models here for Alembic detection
│   │   └── character.py       # Character ORM model
│   ├── routers/               # FastAPI route handlers (to be created)
│   ├── schemas/               # Pydantic request/response schemas (to be created)
│   ├── services/              # Business logic layer (to be created)
│   └── main.py                # FastAPI app entry point
├── alembic/
│   ├── env.py                 # Alembic env (imports app.models for metadata)
│   └── versions/              # Migration files
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── poetry.lock
└── .env                       # Environment variables (not committed)
```

## Development Guidelines

### Database & Migrations
- All ORM models must inherit from `Base` (from `app.core.database`)
- Every new model must be imported in `app/models/__init__.py` so Alembic detects it
- Generate migrations: `docker compose exec scrapper-service alembic revision --autogenerate -m "description"`
- Apply migrations: `docker compose exec scrapper-service alembic upgrade head`
- Migrations run automatically on container startup via docker-compose command

### Docker
- Build/rebuild: `docker compose up --build -d`
- DB is accessible from host on port **5433** (mapped from internal 5432)
- Services communicate internally via `scrapper-network` using service names as hostnames
- Volume mappings sync `app/`, `alembic/`, and `alembic.ini` to host for live development

### Code Style
- Follow existing patterns: SQLAlchemy models in `app/models/`, config in `app/core/`
- Use type hints throughout
- Pydantic schemas for API request/response validation
- Service layer for business logic, routers for HTTP endpoints
- Keep FastAPI dependency injection pattern (e.g., `Depends(get_db)`)

### Environment Variables
- Defined in `.env` file at project root
- `DB_HOST=scrapper-service-db` for Docker internal communication
- Use `127.0.0.1:5433` when connecting from host machine (e.g., PyCharm DB tool)

### Testing
- Tests should be runnable both locally and in Docker
- Use pytest as the test framework
- Mock external HTTP calls (tibiantis.online scraping) in tests

### Adding New Features
1. Create model in `app/models/` and import in `app/models/__init__.py`
2. Create Pydantic schemas in `app/schemas/`
3. Create service logic in `app/services/`
4. Create router in `app/routers/` and register in `app/main.py`
5. Generate and apply Alembic migration
6. Add tests

---

## Interaction Rules (AI Assistant Role)

You are a programming assistant/senior developer acting as a mentor. Your role is to monitor progress, identify areas for improvement, and provide strategic guidance rather than direct implementation.
- **Guidance, Not Code**: Do not provide ready-to-use code blocks unless specifically requested. Instead, point to the libraries, patterns, or specific logic that should be applied.
- **Incremental Steps**: Changes and progress should be made in small, manageable steps.
- **User Approval**: Always wait for user confirmation and a clear signal to proceed to the next step or task.
- **Code Review**: Critically analyze the user's implementation and suggest improvements based on best practices (FastAPI, SQLAlchemy, AsyncIO).

---

## 2-Week Development Plan

> **Start date:** 2026-03-09 (Monday) — **End date:** 2026-03-20 (Friday)

### Week 1: Core Scraping & Blacklist CRUD

#### Day 1–2 (Mon–Tue): Character Scraping Service
- [x] Install `httpx` and `beautifulsoup4` (add to `pyproject.toml`)
- [x] Create `app/services/scraper.py` — scrape character page from `https://tibiantis.online/characters/<name>`
- [x] Parse HTML to extract: name, sex, vocation, level, world, residence, house, guild, last_login, account_status
- [x] Create `app/schemas/character.py` — Pydantic schemas (`CharacterCreate`, `CharacterResponse`, `CharacterUpdate`)
- [x] Create `app/services/character.py` — DB operations (get, create, update, upsert character)
- [x] Create `app/routers/character.py` — endpoints:
  - [x] `GET /api/v1/characters/{name}` — fetch from DB or scrape & store
  - [x] `POST /api/v1/characters/scrape` — scrape a character by name and save to DB
- [x] Register router in `app/main.py`
- [ ] Write unit tests for scraper (mock HTTP responses) and character service

#### Day 3–4 (Wed–Thu): Blacklist Model & CRUD
- [x] Create `app/models/blacklist.py` — `BlacklistEntry` model (id, character_name, added_at, is_active, notes)
- [x] Import in `app/models/__init__.py`
- [x] Generate & apply Alembic migration
- [x] Create `app/schemas/blacklist.py` — Pydantic schemas (`BlacklistCreate`, `BlacklistUpdate`, `BlacklistResponse`)
- [x] Create `app/services/blacklist.py` — CRUD operations
- [x] Create `app/routers/blacklist.py` — endpoints:
  - [x] `POST /api/v1/blacklist` — add character to blacklist
  - [x] `GET /api/v1/blacklist` — list all blacklisted characters
  - [x] `DELETE /api/v1/blacklist/{id}` — remove entry
- [x] Register router in `app/main.py`
- [ ] Write tests for blacklist CRUD

#### Day 5 (Fri): Online Status Monitoring
- [x] Create `app/services/online_checker.py` — check if blacklisted characters are currently online (scrape online list from `https://tibiantis.online/?page=whoisonline`)
- [x] Add `is_online` field to `BlacklistEntry`
- [x] Generate & apply migration
- [x] Create endpoint `GET /api/v1/blacklist/online` — return currently online blacklisted characters
- [ ] Write tests for online checking logic

### Week 2: Bedmage Timers, Discord Bot & Polish

#### Day 6–7 (Mon–Tue): Bedmage Timer Model & Logic
- [ ] Create `app/models/bedmage_timer.py` — `BedmageTimer` model (id, character_name, timer_minutes, is_active, created_at, last_triggered_at)
- [ ] Import in `app/models/__init__.py`
- [ ] Generate & apply Alembic migration
- [ ] Create `app/schemas/bedmage_timer.py` — Pydantic schemas
- [ ] Create `app/services/bedmage_timer.py` — CRUD + timer check logic (compare `last_login` + `timer_minutes` against current time)
- [ ] Create `app/routers/bedmage_timer.py` — endpoints:
  - [ ] `POST /api/v1/bedmage-timers` — create timer for a character
  - [ ] `GET /api/v1/bedmage-timers` — list all timers
  - [ ] `PUT /api/v1/bedmage-timers/{id}` — update timer
  - [ ] `DELETE /api/v1/bedmage-timers/{id}` — delete timer
- [ ] Register router in `app/main.py`
- [ ] Write tests for timer logic

#### Day 8–9 (Wed–Thu): Discord Integration & Background Tasks
- [ ] Add `discord.py` or `aiohttp` for Discord webhook support to `pyproject.toml`
- [ ] Add `DISCORD_WEBHOOK_URL` (and optionally `DISCORD_BOT_TOKEN`) to `Settings` and `.env`
- [ ] Create `app/services/discord_notifier.py` — send notifications via Discord webhook
- [ ] Create `app/services/scheduler.py` — background task (using FastAPI `BackgroundTasks` or `APScheduler`):
  - [ ] Periodically check all active bedmage timers
  - [ ] For each timer: scrape character's `last_login`, check if `timer_minutes` has elapsed
  - [ ] If elapsed and not already triggered: send Discord notification and update `last_triggered_at`
- [ ] Integrate scheduler startup in `app/main.py` (lifespan event)
- [ ] Write tests for Discord notifier (mock webhook calls) and scheduler logic

#### Day 10 (Fri): Testing, Documentation & Cleanup
- [ ] Add `pytest`, `pytest-asyncio`, `httpx` (for test client) to dev dependencies
- [ ] Create `tests/` directory with `conftest.py` (test DB session, test client fixtures)
- [ ] Ensure all existing tests pass in Docker: `docker compose exec scrapper-service pytest`
- [ ] Add error handling & input validation across all endpoints
- [ ] Update `README.md` with:
  - [ ] Project description and features
  - [ ] Setup instructions (Docker, .env)
  - [ ] API endpoint documentation
  - [ ] How to run tests
- [ ] Review and clean up code (remove unused imports, ensure consistent style)

### Future Features (Backlog)
- [ ] Periodic auto-scraping of all tracked characters (cron-style scheduler)
- [ ] Character level-up tracking & notifications
- [ ] Guild monitoring (track all members of a guild)
- [ ] Web dashboard (frontend) for managing blacklist and timers
- [ ] Rate limiting on scraping to avoid overloading tibiantis.online
- [ ] Authentication for API endpoints
- [ ] Logging & monitoring (structured logs, health metrics)
- [ ] Push linting (pre-push hooks with `ruff` or `flake8` for code quality checks)
- [ ] GitHub Actions CI pipeline:
  - [ ] Run linting (`ruff check`) on every push/PR
  - [ ] Run tests (`pytest`) on every push/PR
  - [ ] Build Docker image to verify Dockerfile integrity
  - [ ] Run Alembic migrations check (ensure no pending migrations)
