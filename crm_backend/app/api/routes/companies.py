from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.crud.company import get_company, list_companies

router=APIRouter(prefix="/companies",tags=["Companies"])

@router.get("",response_model=list[CompanyResponse])
async def companies(page:int=1,limit:int=20,search:str|None=None,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    return await list_companies(db,(page-1)*limit,min(limit,100),search)

@router.get("/{company_id}",response_model=CompanyResponse)
async def company(company_id:int,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=await get_company(db,company_id)
    if not obj: raise HTTPException(404,"Company not found")
    return obj

@router.post("",response_model=CompanyResponse,status_code=201)
async def create(data:CompanyCreate,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=Company(**data.model_dump()); db.add(obj); await db.commit(); await db.refresh(obj); return obj

@router.patch("/{company_id}",response_model=CompanyResponse)
async def update(company_id:int,data:CompanyUpdate,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=await get_company(db,company_id)
    if not obj: raise HTTPException(404,"Company not found")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(obj,k,v)
    await db.commit(); await db.refresh(obj); return obj

@router.delete("/{company_id}",status_code=204)
async def delete(company_id:int,db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    obj=await get_company(db,company_id)
    if not obj: raise HTTPException(404,"Company not found")
    try:
        await db.delete(obj); await db.commit()
    except Exception:
        await db.rollback(); raise HTTPException(409,"Company cannot be deleted because it is referenced by CRM records")
