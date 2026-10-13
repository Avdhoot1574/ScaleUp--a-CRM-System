from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Activity
from app.models.company import Company
from app.models.contact import Contact
from app.models.deal import Deal
from app.models.lead import Lead
from app.schemas.activity import ActivityCreate

async def validate_target(db: AsyncSession, data: ActivityCreate) -> None:
    target_map = [(data.lead_id, Lead), (data.contact_id, Contact), (data.company_id, Company), (data.deal_id, Deal)]
    for target_id, model in target_map:
        if target_id is not None and not await db.get(model, target_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model.__name__} with ID {target_id} not found")

async def create_activity(db: AsyncSession, user_id: int, data: ActivityCreate) -> Activity:
    await validate_target(db, data)
    activity = Activity(user_id=user_id, **data.model_dump())
    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity
