from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.company import Company

async def get_company(db: AsyncSession, company_id: int): return await db.get(Company, company_id)
async def list_companies(db: AsyncSession, offset: int, limit: int, search: str | None = None):
    stmt=select(Company)
    if search: stmt=stmt.where(or_(Company.name.ilike(f"%{search}%"), Company.email.ilike(f"%{search}%")))
    return (await db.scalars(stmt.order_by(Company.id.desc()).offset(offset).limit(limit))).all()
