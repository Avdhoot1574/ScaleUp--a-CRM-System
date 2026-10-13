from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company import Company
from app.models.contact import Contact
from app.models.deal import Deal, DealStage
from app.models.lead import Lead, LeadStatus
from app.models.user import User
from app.schemas.deal import DealCreate
from app.schemas.lead import LeadCreate
from app.services.deal_service import probability_for_stage

async def validate_lead_refs(db: AsyncSession, company_id: int, contact_id: int, assigned_to: int) -> None:
    company = await db.get(Company, company_id)
    contact = await db.get(Contact, contact_id)
    user = await db.get(User, assigned_to)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if contact.company_id != company_id:
        raise HTTPException(status_code=400, detail="Contact does not belong to the selected company")
    if not user or not user.is_active:
        raise HTTPException(status_code=404, detail="Assigned user not found or inactive")

async def convert_lead(db: AsyncSession, lead: Lead) -> Deal:
    if lead.status == LeadStatus.CONVERTED:
        raise HTTPException(status_code=409, detail="Lead is already converted")
    deal = Deal(title=f"Deal - {lead.name}", company_id=lead.company_id, contact_id=lead.contact_id, assigned_to=lead.assigned_to, value=0, currency="INR", stage=DealStage.NEW, probability=probability_for_stage(DealStage.NEW))
    db.add(deal)
    lead.status = LeadStatus.CONVERTED
    await db.flush()
    return deal
