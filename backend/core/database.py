from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession
from core.config import settings
from core.base_model import Base

# Handle SQLite specific connection arguments if using SQLite
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    future=True,
    connect_args=connect_args
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependency to get DB session in FastAPI endpoints
async def get_db():
    async with async_session_maker() as session:
        yield session
