# PDF Nomad

An API-first SaaS backend for dynamic PDF extraction, template metadata formatting, and compilation — with a frontend for managing templates and generating PDFs.

## Monorepo Structure

```
PdfNomad/
├── backend/          # FastAPI + SQLAlchemy (SQLite)
│   ├── core/         # Config, database engine
│   ├── models/       # SQLAlchemy ORM models
│   ├── routers/      # API route handlers
│   ├── schemas/      # Pydantic request/response schemas
│   ├── services/     # Business logic (auth, extraction, rendering)
│   ├── utils/        # Security, exceptions
│   ├── main.py       # FastAPI app entry point
│   ├── pyproject.toml
│   ├── Dockerfile
│   └── ...
├── frontend/         # React + Vite + TypeScript (planned)
│   └── README.md
├── docker-compose.yml
└── README.md
```

## Quick Start

### Docker (Recommended)

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

### Backend (Local Development)

```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Full health check (includes DB status) |
| GET | `/health/live` | Liveness probe |
| POST | `/api/v1/auth/signup` | Create a new account |
| POST | `/api/v1/auth/login` | Authenticate and get JWT |
| GET | `/api/v1/auth/me` | Get current user profile |
| POST | `/api/v1/templates/` | Create a template |
| GET | `/api/v1/templates/` | List user templates |
| GET | `/api/v1/templates/{id}` | Get a specific template |
| DELETE | `/api/v1/templates/{id}` | Delete a template |
| POST | `/api/v1/generator/extract` | Extract data from a PDF |
| POST | `/api/v1/generator/render` | Generate a PDF from template + data |

## Environment Variables

See `backend/.env.example` for all available configuration options.
