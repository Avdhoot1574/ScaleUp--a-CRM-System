from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.company import Company
from app.models.contact import Contact
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from app.crud.contact import get_contact, list_contacts

router=APIRouter(prefix="/contacts",tags=["Contacts"])

@router.get("",response_model=list[ContactResponse])
async def contacts(page:int=1,limit:int=20,search:str|None=None,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    return await list_contacts(db,(page-1)*limit,min(limit,100),search)

@router.get("/{contact_id}",response_model=ContactResponse)
async def contact(contact_id:int,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=await get_contact(db,contact_id)
    if not obj: raise HTTPException(404,"Contact not found")
    return obj

@router.post("",response_model=ContactResponse,status_code=201)
async def create(data:ContactCreate,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    if not await db.get(Company,data.company_id): raise HTTPException(404,"Company not found")
    obj=Contact(**data.model_dump()); db.add(obj); await db.commit(); await db.refresh(obj); return obj

@router.patch("/{contact_id}",response_model=ContactResponse)
async def update(contact_id:int,data:ContactUpdate,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=await get_contact(db,contact_id)
    if not obj: raise HTTPException(404,"Contact not found")
    if data.company_id is not None and not await db.get(Company,data.company_id): raise HTTPException(404,"Company not found")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    await db.commit(); await db.refresh(obj); return obj

@router.delete("/{contact_id}",status_code=204)
async def delete(contact_id:int,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=await get_contact(db,contact_id)
    if not obj: raise HTTPException(404,"Contact not found")
    try: await db.delete(obj); await db.commit()
    except Exception:
        await db.rollback(); raise HTTPException(409,"Contact cannot be deleted because it is referenced by CRM records")
