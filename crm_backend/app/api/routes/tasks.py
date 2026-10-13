from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.models.lead import Lead
from app.models.contact import Contact
from app.models.deal import Deal
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.crud.task import get_task, list_tasks

router=APIRouter(prefix="/tasks",tags=["Tasks"])

async def validate_targets(db,data):
    for model,key in [(Lead,"lead_id"),(Contact,"contact_id"),(Deal,"deal_id")]:
        value=getattr(data,key,None)
        if value is not None and not await db.get(model,value): raise HTTPException(404,f"{model.__name__} not found")
    user=await db.get(User,data.assigned_to)
    if not user or not user.is_active: raise HTTPException(404,"Assigned user not found or inactive")

@router.get("",response_model=list[TaskResponse])
async def tasks(page:int=1,limit:int=20,status:TaskStatus|None=None,assigned_to:int|None=None,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    if current.role.value == "SALES_REP": assigned_to=current.id
    return await list_tasks(db,(page-1)*limit,min(limit,100),status,assigned_to)

@router.get("/{task_id}",response_model=TaskResponse)
async def task(task_id:int,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_task(db,task_id)
    if not obj: raise HTTPException(404,"Task not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can access only tasks assigned to you")
    return obj

@router.post("",response_model=TaskResponse,status_code=201)
async def create(data:TaskCreate,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    if current.role.value == "SALES_REP" and data.assigned_to != current.id: raise HTTPException(403,"Sales representatives can create tasks only for themselves")
    await validate_targets(db,data); obj=Task(**data.model_dump()); db.add(obj); await db.commit(); await db.refresh(obj); return obj

@router.patch("/{task_id}",response_model=TaskResponse)
async def update(task_id:int,data:TaskUpdate,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_task(db,task_id)
    if not obj: raise HTTPException(404,"Task not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can update only tasks assigned to you")
    values=data.model_dump(exclude_unset=True)
    assigned=values.get("assigned_to",obj.assigned_to)
    if current.role.value == "SALES_REP" and assigned != current.id: raise HTTPException(403,"You cannot reassign a task")
    for model,key in [(Lead,"lead_id"),(Contact,"contact_id"),(Deal,"deal_id")]:
        value=values.get(key,getattr(obj,key))
        if value is not None and not await db.get(model,value): raise HTTPException(404,f"{model.__name__} not found")
    user=await db.get(User,assigned)
    if not user or not user.is_active: raise HTTPException(404,"Assigned user not found or inactive")
    for k,v in values.items(): setattr(obj,k,v)
    if values.get("status") == TaskStatus.COMPLETED: obj.completed_at=datetime.now(timezone.utc)
    elif values.get("status") and values["status"] != TaskStatus.COMPLETED: obj.completed_at=None
    await db.commit(); await db.refresh(obj); return obj

@router.delete("/{task_id}",status_code=204)
async def delete(task_id:int,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_task(db,task_id)
    if not obj: raise HTTPException(404,"Task not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can delete only tasks assigned to you")
    await db.delete(obj); await db.commit()
