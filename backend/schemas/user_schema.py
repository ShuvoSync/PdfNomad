# schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from core.enums import AccountType

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    account_type: AccountType = AccountType.INDIVIDUAL  # Enforces "individual" or "business"
    custom_fields: Optional[Dict[str, str]] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileResponse(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    account_type: AccountType
    company_name: Optional[str] = None
    tax_id: Optional[str] = None
    billing_address: Optional[str] = None
    custom_fields: Optional[Dict[str, str]] = None

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

