# models/user_profile.py
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class UserProfile(BaseModel):
    __tablename__ = "user_profiles"

    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Universal fields
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    account_type = Column(String, default="individual", nullable=False)  # "individual" or "business"
    
    # Optional business/professional fields
    company_name = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)          # e.g., VAT / TRN number
    billing_address = Column(String, nullable=True)
    
    # User-defined custom key-value fields (e.g., {"Branch": "HQ", "Project Code": "P-404"})
    custom_fields = Column(JSON, default=dict, nullable=True)

    # Relationship back to User
    user = relationship("User", back_populates="profile")