from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.lead import Lead, LeadPriority, LeadStatus
from app.models.user import User
from app.schemas.lead import LeadConversionResponse, LeadCreate, LeadResponse, LeadUpdate
from app.crud.lead import get_lead, list_leads
from app.services.lead_service import convert_lead, validate_lead_refs

router=APIRouter(prefix="/leads",tags=["Leads"])

@router.get("",response_model=list[LeadResponse])
async def leads(page:int=1,limit:int=20,search:str|None=None,status:LeadStatus|None=None,priority:LeadPriority|None=None,assigned_to:int|None=None,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    if current.role.value == "SALES_REP": assigned_to=current.id
    return await list_leads(db,(page-1)*limit,min(limit,100),search,status,priority,assigned_to)

@router.get("/{lead_id}",response_model=LeadResponse)
async def lead(lead_id:int,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_lead(db,lead_id)
    if not obj: raise HTTPException(404,"Lead not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can access only leads assigned to you")
    return obj

@router.post("",response_model=LeadResponse,status_code=201)
async def create(data:LeadCreate,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    if current.role.value == "SALES_REP" and data.assigned_to != current.id: raise HTTPException(403,"Sales representatives can create leads only for themselves")
    await validate_lead_refs(db,data.company_id,data.contact_id,data.assigned_to)
    obj=Lead(**data.model_dump()); db.add(obj); await db.commit(); await db.refresh(obj); return obj

@router.patch("/{lead_id}",response_model=LeadResponse)
async def update(lead_id:int,data:LeadUpdate,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_lead(db,lead_id)
    if not obj: raise HTTPException(404,"Lead not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can update only leads assigned to you")
    values=data.model_dump(exclude_unset=True)
    company_id=values.get("company_id",obj.company_id); contact_id=values.get("contact_id",obj.contact_id); assigned=values.get("assigned_to",obj.assigned_to)
    if current.role.value == "SALES_REP" and assigned != current.id: raise HTTPException(403,"You cannot reassign a lead")
    await validate_lead_refs(db,company_id,contact_id,assigned)
    for k,v in values.items(): setattr(obj,k,v)
    await db.commit(); await db.refresh(obj); return obj

@router.post("/{lead_id}/convert",response_model=LeadConversionResponse)
async def convert(lead_id:int,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_lead(db,lead_id)
    if not obj: raise HTTPException(404,"Lead not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can convert only leads assigned to you")
    deal=await convert_lead(db,obj); await db.commit(); await db.refresh(obj); await db.refresh(deal)
    return {"lead":obj,"deal_id":deal.id}

@router.delete("/{lead_id}",status_code=204)
async def delete(lead_id:int,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_lead(db,lead_id)
    if not obj: raise HTTPException(404,"Lead not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can delete only leads assigned to you")
    await db.delete(obj); await db.commit()
