from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from datetime import datetime, timezone
from core.base_model import BaseModel

class GenerationLog(BaseModel):
    __tablename__ = "generation_logs"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    template_id = Column(String(36), ForeignKey("templates.id"), nullable=True)
    
    status = Column(String, default="success")  # success, failed
    metadata_snapshot = Column(JSON, nullable=True) # Optional snapshot of data used