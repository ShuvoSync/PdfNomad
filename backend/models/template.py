from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class Template(BaseModel):
    __tablename__ = "templates"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True, nullable=False)

    # JSON column for user-defined extraction rules & layout formats (maps to JSONB in Postgres)
    extraction_schema = Column(JSON, nullable=True)
    layout_schema = Column(JSON, nullable=False)

    # Relationship back to User
    user = relationship("User", back_populates="templates")
