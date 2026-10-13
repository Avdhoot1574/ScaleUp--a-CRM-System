from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lead import Lead, LeadPriority, LeadStatus

async def get_lead(db: AsyncSession, lead_id: int): return await db.get(Lead, lead_id)
async def list_leads(db: AsyncSession, offset: int, limit: int, search=None, status=None, priority=None, assigned_to=None):
    stmt=select(Lead)
    if search: stmt=stmt.where(or_(Lead.name.ilike(f"%{search}%"), Lead.email.ilike(f"%{search}%")))
    if status: stmt=stmt.where(Lead.status == status)
    if priority: stmt=stmt.where(Lead.priority == priority)
    if assigned_to: stmt=stmt.where(Lead.assigned_to == assigned_to)
    return (await db.scalars(stmt.order_by(Lead.id.desc()).offset(offset).limit(limit))).all()
