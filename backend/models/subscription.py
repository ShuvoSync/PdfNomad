from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime , JSON , UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from core.base_model import BaseModel

class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    user_id = Column(UUID, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Plan info & Status
    plan_name = Column(String, default="free")             # free, pro, enterprise
    status = Column(String, default="active")              # active, canceled, past_due, unpaid
    
    # Billing Lifecycle Dates
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)   # Next renewal date
    
    # Cancellation handling
    cancel_at_period_end = Column(Boolean, default=False)  # True if user canceled, but keeps access until period ends
    
    # Grace Period for failed payments (e.g., 3-5 days after period_end)
    grace_period_end = Column(DateTime, nullable=True)
    
    # Payment Gateway Reference (Stripe/LemonSqueezy ID)
    gateway_subscription_id = Column(String, nullable=True, unique=True)
    
    user = relationship("User", back_populates="subscription")
