from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from routers import auth, templates, generator, health

app = FastAPI(
    title="PDF Nomad API",
    description="A SaaS backend for dynamic PDF extraction, template metadata formatting, and compilation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow frontend dev server + mobile/Termux access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*",  # Allow all origins for mobile dev (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Automatically create database tables on startup (great for local mobile SQLite testing)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include Routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(templates.router, prefix="/api/v1/templates", tags=["Templates & Layouts"])
app.include_router(generator.router, prefix="/api/v1/generator", tags=["PDF Generation & Extraction"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to PDF Nomad API", "docs": "/docs", "status": "active"}
