from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from datetime import datetime, timezone
from core.database import Base

class GenerationLog(Base):
    __tablename__ = "generation_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    
    status = Column(String, default="success")  # success, failed
    metadata_snapshot = Column(JSON, nullable=True) # Optional snapshot of data used
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
