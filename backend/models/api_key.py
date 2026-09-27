from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime , JSON, UUID
from datetime import datetime, timezone
from core.base_model import BaseModel

class APIKey(BaseModel):
    __tablename__ = "api_keys"
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    key_hash = Column(String, unique=True, index=True, nullable=False)  # Hashed API key
    name = Column(String, nullable=False)                               # e.g., "Production Bot Key"