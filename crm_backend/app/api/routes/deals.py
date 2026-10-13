from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.company import Company
from app.models.contact import Contact
from app.models.deal import Deal, DealStage
from app.models.user import User
from app.schemas.deal import DealCreate, DealResponse, DealUpdate
from app.crud.deal import get_deal, list_deals
from app.services.deal_service import probability_for_stage

router=APIRouter(prefix="/deals",tags=["Deals"])

async def validate_refs(db,company_id,contact_id,assigned_to):
    company=await db.get(Company,company_id); contact=await db.get(Contact,contact_id); user=await db.get(User,assigned_to)
    if not company: raise HTTPException(404,"Company not found")
    if not contact: raise HTTPException(404,"Contact not found")
    if contact.company_id != company_id: raise HTTPException(400,"Contact does not belong to the selected company")
    if not user or not user.is_active: raise HTTPException(404,"Assigned user not found or inactive")

@router.get("",response_model=list[DealResponse])
async def deals(page:int=1,limit:int=20,search:str|None=None,stage:DealStage|None=None,assigned_to:int|None=None,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    if current.role.value == "SALES_REP": assigned_to=current.id
    return await list_deals(db,(page-1)*limit,min(limit,100),search,stage,assigned_to)

@router.get("/{deal_id}",response_model=DealResponse)
async def deal(deal_id:int,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_deal(db,deal_id)
    if not obj: raise HTTPException(404,"Deal not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can access only deals assigned to you")
    return obj

@router.post("",response_model=DealResponse,status_code=201)
async def create(data:DealCreate,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    if current.role.value == "SALES_REP" and data.assigned_to != current.id: raise HTTPException(403,"Sales representatives can create deals only for themselves")
    await validate_refs(db,data.company_id,data.contact_id,data.assigned_to)
    obj=Deal(**data.model_dump(exclude={"probability"}),currency="INR",probability=probability_for_stage(data.stage,data.probability)); db.add(obj); await db.commit(); await db.refresh(obj); return obj

@router.patch("/{deal_id}",response_model=DealResponse)
async def update(deal_id:int,data:DealUpdate,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_deal(db,deal_id)
    if not obj: raise HTTPException(404,"Deal not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can update only deals assigned to you")
    values=data.model_dump(exclude_unset=True); company_id=values.get("company_id",obj.company_id); contact_id=values.get("contact_id",obj.contact_id); assigned=values.get("assigned_to",obj.assigned_to)
    if current.role.value == "SALES_REP" and assigned != current.id: raise HTTPException(403,"You cannot reassign a deal")
    await validate_refs(db,company_id,contact_id,assigned)
    if "stage" in values and "probability" not in values: values["probability"]=probability_for_stage(values["stage"])
    for k,v in values.items(): setattr(obj,k,v)
    await db.commit(); await db.refresh(obj); return obj

@router.delete("/{deal_id}",status_code=204)
async def delete(deal_id:int,db:AsyncSession=Depends(get_db),current:User=Depends(get_current_user)):
    obj=await get_deal(db,deal_id)
    if not obj: raise HTTPException(404,"Deal not found")
    if current.role.value == "SALES_REP" and obj.assigned_to != current.id: raise HTTPException(403,"You can delete only deals assigned to you")
    await db.delete(obj); await db.commit()
