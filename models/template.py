from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.database import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    
    # JSON column for user-defined extraction rules & layout formats (maps to JSONB in Postgres)
    extraction_schema = Column(JSON, nullable=True)
    layout_schema = Column(JSON, nullable=False)
