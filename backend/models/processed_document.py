# models/processed_document.py
from sqlalchemy import Column, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class ProcessedDocument(BaseModel):
    __tablename__ = "processed_documents"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    original_filename = Column(String, nullable=False)
    new_filename = Column(String, nullable=True)            # After automatic renaming
    file_path = Column(String, nullable=False)              # Final saved path
    status = Column(String, default="success", nullable=False)  # success, failed, needs_review
    extracted_data = Column(JSON, default=dict, nullable=True)  # Extracted invoice number, date, amount, etc.
    
    # Relationship back to User
    user = relationship("User", backref="processed_documents")
