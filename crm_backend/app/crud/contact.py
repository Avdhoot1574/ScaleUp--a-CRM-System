from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact import Contact

async def get_contact(db: AsyncSession, contact_id: int): return await db.get(Contact, contact_id)
async def list_contacts(db: AsyncSession, offset: int, limit: int, search: str | None = None):
    stmt=select(Contact)
    if search: stmt=stmt.where(or_(Contact.name.ilike(f"%{search}%"), Contact.email.ilike(f"%{search}%")))
    return (await db.scalars(stmt.order_by(Contact.id.desc()).offset(offset).limit(limit))).all()
