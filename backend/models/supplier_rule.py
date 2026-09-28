# models/supplier_rule.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class SupplierRule(BaseModel):
    __tablename__ = "supplier_rules"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    supplier_name = Column(String, nullable=False)          # e.g., "DEWA" or "Etisalat"
    keyword_identifier = Column(String, nullable=False)     # Text to search for in the PDF
    target_folder = Column(String, nullable=False)          # Local folder path to move sorted files
    
    # Relationship back to User
    user = relationship("User", backref="supplier_rules")
