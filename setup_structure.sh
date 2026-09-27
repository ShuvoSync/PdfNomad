#!/bin/bash

echo "🚀 Setting up PDF Nomad directory structure..."

# 1. Create directories
mkdir -p core models schemas routers services utils

# 2. Create Python package init files
touch core/__init__.py
touch models/__init__.py
touch schemas/__init__.py
touch routers/__init__.py
touch services/__init__.py
touch utils/__init__.py

# 3. Create basic starter files
cat << 'EOF' > main.py
from fastapi import FastAPI

app = FastAPI(title="PDF Nomad API", version="1.0")

@app.get("/")
def root():
    return {"status": "PDF Nomad API is running"}
EOF

cat << 'EOF' > core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PDF Nomad"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/pdfnomad"

    class Config:
        env_file = ".env"

settings = Settings()
EOF

cat << 'EOF' > core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

async def get_db():
    async with async_session_maker() as session:
        yield session
EOF

# Create empty module files so they are ready for your code
touch models/user.py models/template.py
touch schemas/user_schema.py schemas/template_schema.py
touch routers/auth.py routers/templates.py routers/generator.py
touch services/auth_service.py services/extractor_engine.py services/renderer_engine.py
touch utils/exceptions.py utils/security.py

echo "✅ Project structure successfully created!"
