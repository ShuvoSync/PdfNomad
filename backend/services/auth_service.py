# routers/auth.py (or wherever your auth endpoints live)
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.config import settings
from core.database import get_db
from models.user import User
from models.user_profile import UserProfile
from core.security import hash_password, verify_password, create_access_token, create_password_reset_token, verify_password_reset_token , get_current_user
from schemas.user_schema import (
    PasswordChangeRequest, ForgotPasswordRequest, 
    ResetPasswordRequest, SetPasswordRequest, SocialLoginRequest, Token
)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

# 1. UPDATED LOGIN (Handles null passwords for social accounts)
@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    # If user has no password (social account) or password doesn't match, reject login
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password, or account uses social login.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# 2. CHANGE PASSWORD (Logged-in user knows old password)
@router.post("/change-password")
async def change_password(
    body: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user.hashed_password or not verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password.")
    
    current_user.hashed_password = hash_password(body.new_password)
    db.add(current_user)
    await db.commit()
    return {"message": "Password updated successfully."}


# 3. SET PASSWORD (For social login users adding a password)
@router.post("/set-password")
async def set_password(
    body: SetPasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.hashed_password is not None:
        raise HTTPException(status_code=400, detail="Password already set. Use change-password instead.")
    
    current_user.hashed_password = hash_password(body.new_password)
    db.add(current_user)
    await db.commit()
    return {"message": "Password successfully created for your account."}


# 4. FORGOT PASSWORD (Requests token)
@router.post("/forgot-password")
async def forgot_password(body: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    
    if user:
        # Generate short-lived reset token (15 mins)
        reset_token = create_password_reset_token(user.email)
        # TODO: Send email with reset token in production
        print(f"[DEBUG] Password Reset Token for {user.email}: {reset_token}")
        
    return {"message": "If the email exists, a password reset link has been sent."}


# 5. RESET PASSWORD (Using the token)
@router.post("/reset-password")
async def reset_password(body: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    email = verify_password_reset_token(body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired password reset token.")
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user.hashed_password = hash_password(body.new_password)
    db.add(user)
    await db.commit()
    return {"message": "Password has been successfully reset."}


# 6. SOCIAL LOGIN (Google / Third-party callback)
@router.post("/social-login", response_model=Token)
async def social_login(body: SocialLoginRequest, db: AsyncSession = Depends(get_db)):
    # Verify token with provider (e.g., Google API call) -> extract email & name
    email = "verified_user@gmail.com"  # Mocked result from provider verification
    full_name = "Social User"
    
    if not email:
        raise HTTPException(status_code=400, detail="Social authentication failed.")
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    if not user:
        # Create user with NO password (hashed_password = None)
        user = User(email=email, hashed_password=None)
        db.add(user)
        await db.flush()
        
        profile = UserProfile(user_id=user.id, full_name=full_name, account_type="individual")
        db.add(profile)
        await db.commit()
        await db.refresh(user)

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}