from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from models.user import User
from models.user_profile import UserProfile
from models.subscription import Subscription
from models.limitation import UserLimitation
from schemas.user_schema import UserCreate, LoginRequest, UserResponse, Token
from services.auth_service import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

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

    # 2. Create User Profile (Name, Company)
    new_profile = UserProfile(
        user_id=new_user.id,
        full_name=user_in.full_name,
        company_name=user_in.company_name
    )
    
    # 3. Setup Subscriptions & Limitations
    new_sub = Subscription(user_id=new_user.id, plan_name="free", status="active")
    new_limit = UserLimitation(user_id=new_user.id, tier="free", max_monthly_generations=20)

    db.add(new_profile)
    db.add(new_sub)
    db.add(new_limit)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
async def login(user_in: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Issue real JWT Token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Load user with profile relationship using selectinload for async compatibility
    from sqlalchemy.orm import selectinload
    result = await db.execute(
        select(User).options(selectinload(User.profile)).where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()
    return user
