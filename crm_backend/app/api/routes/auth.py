from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import authenticate_user, issue_access_token, register_user

router=APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data:RegisterRequest, db:AsyncSession=Depends(get_db)):
    count=await db.scalar(select(func.count(User.id))) or 0
    user=await register_user(db,data)
    if count == 0:
        user.role=UserRole.ADMIN
        await db.commit(); await db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(data:LoginRequest, db:AsyncSession=Depends(get_db)):
    user=await authenticate_user(db,data)
    return TokenResponse(access_token=issue_access_token(user))

@router.get("/me", response_model=UserResponse)
async def me(current_user:User=Depends(get_current_user)):
    return current_user
