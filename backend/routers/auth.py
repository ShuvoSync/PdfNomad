from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core.database import get_db
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token,
    get_current_user,
)
from models.user import User
from models.user_profile import UserProfile
from models.subscription import Subscription
from models.limitation import UserLimitation
from schemas.user_schema import (
    UserCreate,
    LoginRequest,
    UserResponse,
    Token,
    PasswordChangeRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    SetPasswordRequest,
    SocialLoginRequest,
)

router = APIRouter()


# ── Signup ──────────────────────────────────────────────
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email is already registered.")

    # 1. Create User
    new_user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # 2. Create User Profile (Name, Company, Account Type, Custom Fields)
    new_profile = UserProfile(
        user_id=new_user.id,
        full_name=user_in.full_name,
        company_name=user_in.company_name,
        account_type=user_in.account_type.value,
        custom_fields=user_in.custom_fields,
    )

    # 3. Setup Subscriptions & Limitations
    new_sub = Subscription(user_id=new_user.id, plan_name="free", status="active")
    new_limit = UserLimitation(user_id=new_user.id, tier="free", max_monthly_generations=20)

    db.add(new_profile)
    db.add(new_sub)
    db.add(new_limit)
    await db.commit()
    await db.refresh(new_user)

    # 4. Load profile relationship for response
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.id == new_user.id)
    )
    return result.scalar_one()


# ── Login ────────────────────────────────────────────────
@router.post("/login", response_model=Token)
async def login(user_in: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalar_one_or_none()

    # Reject if user doesn't exist, has no password (social account), or password doesn't match
    if not user or not user.hashed_password or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password, or account uses social login.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# ── Get Current User ────────────────────────────────────
@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    return user


# ── Change Password (Logged-in user knows old password) ──
@router.post("/change-password")
async def change_password(
    body: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.hashed_password or not verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password.")

    current_user.hashed_password = hash_password(body.new_password)
    db.add(current_user)
    await db.commit()
    return {"message": "Password updated successfully."}


# ── Set Password (For social login users adding a password) ──
@router.post("/set-password")
async def set_password(
    body: SetPasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.hashed_password is not None:
        raise HTTPException(status_code=400, detail="Password already set. Use change-password instead.")

    current_user.hashed_password = hash_password(body.new_password)
    db.add(current_user)
    await db.commit()
    return {"message": "Password successfully created for your account."}


# ── Forgot Password (Requests token) ─────────────────────
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


# ── Reset Password (Using the token) ─────────────────────
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


# ── Social Login (Google / Third-party callback) ─────────
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


# ── Logout ───────────────────────────────────────────────
@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Client-side logout endpoint. The client should discard the token.
    In a more advanced setup, this could blacklist the token.
    """
    return {"message": "Successfully logged out."}
