from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.dependencies import require_roles
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.security import hash_password
from app.crud.user import get_user, list_users

router=APIRouter(prefix="/users", tags=["Users"])

@router.get("", response_model=list[UserResponse])
async def users(page:int=1, limit:int=20, db:AsyncSession=Depends(get_db), _:User=Depends(require_roles(UserRole.ADMIN))):
    return await list_users(db,(page-1)*limit,min(limit,100))

@router.get("/{user_id}", response_model=UserResponse)
async def user_detail(user_id:int, db:AsyncSession=Depends(get_db), _:User=Depends(require_roles(UserRole.ADMIN))):
    user=await get_user(db,user_id)
    if not user: raise HTTPException(404,"User not found")
    return user

@router.post("", response_model=UserResponse, status_code=201)
async def create_user(data:UserCreate, db:AsyncSession=Depends(get_db), _:User=Depends(require_roles(UserRole.ADMIN))):
    existing=await db.scalar(select(User).where(User.email==data.email.lower()))
    if existing: raise HTTPException(409,"Email is already registered")
    user=User(name=data.name.strip(),email=data.email.lower(),password_hash=hash_password(data.password),role=data.role)
    db.add(user); await db.commit(); await db.refresh(user); return user

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id:int, data:UserUpdate, db:AsyncSession=Depends(get_db), _:User=Depends(require_roles(UserRole.ADMIN))):
    user=await get_user(db,user_id)
    if not user: raise HTTPException(404,"User not found")
    for key,value in data.model_dump(exclude_unset=True).items(): setattr(user,key,value)
    await db.commit(); await db.refresh(user); return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id:int, db:AsyncSession=Depends(get_db), current_user:User=Depends(require_roles(UserRole.ADMIN))):
    user=await get_user(db,user_id)
    if not user: raise HTTPException(404,"User not found")
    if user.id == current_user.id: raise HTTPException(400,"You cannot delete your own account")
    await db.delete(user); await db.commit()
