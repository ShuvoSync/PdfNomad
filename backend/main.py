from fastapi import FastAPI
from core.database import engine, Base
from routers import auth, templates, generator, health

app = FastAPI(
    title="PDF Nomad API",
    description="A SaaS backend for dynamic PDF extraction, template metadata formatting, and compilation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
