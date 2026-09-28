# PDF Nomad

An API-first SaaS backend for dynamic PDF extraction, template metadata formatting, and compilation — with a frontend for managing templates and generating PDFs.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start (All Platforms)](#quick-start-all-platforms)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: PC / Laptop (Local Development)](#option-2-pc--laptop-local-development)
  - [Option 3: Android (Termux)](#option-3-android-termux)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Platform | Requirements |
|----------|-------------|
| **Docker** | Docker Engine 24+ and Docker Compose v2+ |
| **PC (Windows/macOS/Linux)** | Python 3.12+ and [uv](https://docs.astral.sh/uv/getting-started/installation/) |
| **Android (Termux)** | [Termux](https://f-droid.org/en/packages/com.termux/) (F-Droid version recommended) |

---

## Quick Start (All Platforms)

### Option 1: Docker (Recommended)

The fastest way to run PdfNomad — no Python setup required.

```bash
# Clone the repository
git clone https://github.com/your-username/PdfNomad.git
cd PdfNomad

# Start the backend
docker compose up --build
```

The API will be available at:

- **API:** http://localhost:8000
- **Interactive Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

To run in the background:

```bash
docker compose up --build -d
```

To stop:

```bash
docker compose down
```

To stop and delete the database volume (full reset):

```bash
docker compose down -v
```

---

### Option 2: PC / Laptop (Local Development)

Works on **Windows**, **macOS**, and **Linux**.

#### Step 1: Install uv

**Linux / macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Or install via pip (any platform):**

```bash
pip install uv
```

#### Step 2: Clone and Run

```bash
# Clone the repository
git clone https://github.com/your-username/PdfNomad.git
cd PdfNomad/backend

# Install dependencies (uv creates a .venv automatically)
uv sync

# Start the development server with auto-reload
uv run uvicorn main:app --reload
```

The API will be available at http://localhost:8000 with docs at `/docs`.

#### Alternative: Without uv (using pip + venv)

If you prefer not to use `uv`:

```bash
cd backend

# Create a virtual environment
python -m venv .venv

# Activate it
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

> **Note:** If you don't have a `requirements.txt`, generate one with `uv pip freeze > requirements.txt` or install packages manually:
> ```bash
> pip install "fastapi[standard]" "sqlalchemy[asyncio]" aiosqlite pydantic-settings pyjwt passlib bcrypt pypdf reportlab
> ```

---

### Option 3: Android (Termux)

Run PdfNomad directly on your Android device using [Termux](https://f-droid.org/en/packages/com.termux/).

#### Step 1: Install Termux

Install Termux from **F-Droid** (recommended) or GitHub releases. The Play Store version is outdated.

- F-Droid: https://f-droid.org/en/packages/com.termux/
- GitHub: https://github.com/termux/termux-app/releases

#### Step 2: Update Packages and Install Python

Open Termux and run:

```bash
# Update package lists
pkg update -y

# Install Python and required build tools
pkg install -y python python-pip git

# Install uv (optional but recommended)
pip install uv
```

#### Step 3: Clone and Run

```bash
# Clone the repository
git clone https://github.com/your-username/PdfNomad.git
cd PdfNomad/backend

# Install dependencies
uv sync

# Run the server
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` on your device.

To access it from another device on the same Wi-Fi network, find your phone's IP:

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Then open `http://<YOUR_PHONE_IP>:8000` in your browser.

#### Termux Tips

- **Keep Termux alive:** Go to Termux settings > Acquire Wakelock to prevent Android from killing the process.
- **Run in background:** Use `nohup` or `tmux`:
  ```bash
  pkg install tmux
  tmux new -s pdfnomad
  uv run uvicorn main:app --host 0.0.0.0 --port 8000
  # Detach: Ctrl+B then D
  # Reattach: tmux attach -t pdfnomad
  ```
- **Storage access:** Run `termux-setup-storage` if you need to access PDFs from your device storage.

---

## Configuration

All configuration is done via environment variables. Create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env  # if .env.example exists
# or create your own:
nano .env
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PROJECT_NAME` | `"PDF Nomad"` | Application name |
| `DATABASE_URL` | `sqlite+aiosqlite:///./pdfnomad.db` | Database connection string |
| `SECRET_KEY` | `"your-super-secret-key-change-in-production"` | JWT signing key (change in production!) |
| `ALGORITHM` | `"HS256"` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token expiration time (minutes) |

### Example `.env` file

```env
PROJECT_NAME=PDF Nomad
DATABASE_URL=sqlite+aiosqlite:///./pdfnomad.db
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> **Important:** Always change `SECRET_KEY` in production to a long random string.

---

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

Interactive API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

---

## Project Structure

```
PdfNomad/
├── backend/              # FastAPI + SQLAlchemy (SQLite)
│   ├── core/             # Config, database engine, base model, enums
│   ├── models/           # SQLAlchemy ORM models
│   ├── routers/          # API route handlers
│   ├── schemas/          # Pydantic request/response schemas
│   ├── services/         # Business logic (auth, extraction, rendering)
│   ├── utils/            # Security, exceptions
│   ├── main.py           # FastAPI app entry point
│   ├── pyproject.toml    # Python project config & dependencies
│   ├── Dockerfile        # Multi-stage Docker build
│   └── README.md
├── frontend/             # React + Vite + TypeScript (planned)
│   └── README.md
├── docker-compose.yml    # Docker orchestration
└── README.md             # This file
```

---

## Troubleshooting

### Port 8000 is already in use

```bash
# Find what's using port 8000
# Linux/macOS:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Use a different port
uv run uvicorn main:app --port 8001
```

### Docker: permission denied on Docker socket

```bash
# Add your user to the docker group (Linux)
sudo usermod -aG docker $USER
# Log out and log back in for changes to take effect
```

### Termux: server not accessible from other devices

- Make sure you used `--host 0.0.0.0` (not `127.0.0.1`)
- Check that both devices are on the same Wi-Fi network
- Try disabling your phone's firewall or VPN

### Database locked (SQLite)

SQLite doesn't handle concurrent writes well. If you see "database is locked" errors:

- Make sure only one process is accessing the database
- For production, consider switching to PostgreSQL (see `backend/core/config.py` for commented-out config)

### uv: command not found

```bash
# Re-source your shell or add uv to PATH
# Linux/macOS:
source ~/.bashrc  # or ~/.zshrc
# Or add manually:
export PATH="$HOME/.local/bin:$PATH"
```

---

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
