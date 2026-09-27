from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "PDF Nomad"
#    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/pdfnomad"
    DATABASE_URL: str = "sqlite+aiosqlite:///./pdfnomad.db"
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Tells pydantic to load from a .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

