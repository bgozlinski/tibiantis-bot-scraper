# Tibiantis Bot Scraper

A FastAPI-based web scraper and monitoring bot for [tibiantis.online](https://tibiantis.online) character data, with Discord notification capabilities.

## Features

- **Character Scraping** — Scrape and store character data (name, vocation, level, world, etc.) from tibiantis.online
- **Blacklist Management** — CRUD operations for monitoring characters' online status
- **Bedmage Timers** — Configurable timers that trigger Discord notifications after X minutes since a player's last login
- **Discord Notifications** — Real-time alerts via Discord webhook/bot integration

## Tech Stack

- Python 3.13 / FastAPI
- SQLAlchemy 2.x + Alembic (PostgreSQL 17.5)
- Docker + Docker Compose
- Poetry (package management)
- pydantic-settings (configuration)

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- (Optional) [Poetry](https://python-poetry.org/) for local development

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/tibiantis-bot-scraper.git
   cd tibiantis-bot-scraper
   ```

2. **Create a `.env` file** in the project root:
   ```env
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

3. **Start the services:**
   ```bash
   docker compose up --build -d
   ```

   This will:
   - Start PostgreSQL on internal port 5432 (exposed on host port 5433)
   - Run Alembic migrations automatically
   - Start the FastAPI app on port 8000

4. **Verify:**
   - API: [http://localhost:8000/health](http://localhost:8000/health)
   - Docs: [http://localhost:8000/docs](http://localhost:8000/docs)



## Development

### Alembic Migrations

```bash
# Generate a new migration
docker compose exec scrapper-service alembic revision --autogenerate -m "description"

# Apply migrations
docker compose exec scrapper-service alembic upgrade head
```

### Running Tests

```bash
docker compose exec scrapper-service pytest
```

### Project Structure

```
tibiantis-bot-scraper/
├── app/
│   ├── core/           # Config & database setup
│   ├── models/         # SQLAlchemy ORM models
│   ├── routers/        # FastAPI route handlers
│   ├── schemas/        # Pydantic request/response schemas
│   ├── services/       # Business logic layer
│   └── main.py         # FastAPI app entry point
├── alembic/            # Database migrations
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## License

This project is licensed under the [MIT License](LICENSE).
