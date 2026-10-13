from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.deal import Deal, DealStage

async def get_deal(db: AsyncSession, deal_id: int): return await db.get(Deal, deal_id)
async def list_deals(db: AsyncSession, offset: int, limit: int, search=None, stage=None, assigned_to=None):
    stmt=select(Deal)
    if search: stmt=stmt.where(or_(Deal.title.ilike(f"%{search}%"), Deal.description.ilike(f"%{search}%")))
    if stage: stmt=stmt.where(Deal.stage == stage)
    if assigned_to: stmt=stmt.where(Deal.assigned_to == assigned_to)
    return (await db.scalars(stmt.order_by(Deal.id.desc()).offset(offset).limit(limit))).all()
