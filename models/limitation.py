from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from core.database import Base

class UserLimitation(Base):
    __tablename__ = "user_limitations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    tier = Column(String, default="free")  # free, pro, enterprise
    max_monthly_generations = Column(Integer, default=20)  # Free tier cap
    current_usage = Column(Integer, default=0)             # Resets monthly
    
    can_use_custom_templates = Column(Boolean, default=True)
    can_use_api = Column(Boolean, default=False)           # Locked for free tier
    
    reset_date = Column(DateTime, nullable=True)           # When monthly usage resets
    
    user = relationship("User", back_populates="limitation")
