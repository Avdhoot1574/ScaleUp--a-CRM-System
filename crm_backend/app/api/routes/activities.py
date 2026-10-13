from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.activity import Activity
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityResponse
from app.crud.activity import get_activity, list_activities
from app.services.activity_service import create_activity

router=APIRouter(prefix="/activities",tags=["Activities"])

@router.get("",response_model=list[ActivityResponse])
async def activities(page:int=1,limit:int=20,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    return await list_activities(db,(page-1)*limit,min(limit,100))

@router.get("/{activity_id}",response_model=ActivityResponse)
async def activity(activity_id:int,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=await get_activity(db,activity_id)
    if not obj: raise HTTPException(404,"Activity not found")
    return obj

@router.post("",response_model=ActivityResponse,status_code=201)
async def create(data:ActivityCreate,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    return await create_activity(db,current.id,data)
