# schemas/user_schema.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Dict
from core.enums import AccountType

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    account_type: AccountType = AccountType.INDIVIDUAL
    custom_fields: Optional[Dict[str, str]] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# NEW SCHEMAS FOR ADVANCED AUTH
class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class SetPasswordRequest(BaseModel):   # For social login users adding a password
    new_password: str

class SocialLoginRequest(BaseModel):
    provider: str  # e.g., "google"
    token: str     # Access token or ID token from provider

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