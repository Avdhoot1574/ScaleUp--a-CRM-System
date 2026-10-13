from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.activity import Activity

async def list_activities(db: AsyncSession, offset: int, limit: int): return (await db.scalars(select(Activity).order_by(Activity.activity_time.desc()).offset(offset).limit(limit))).all()
async def get_activity(db: AsyncSession, activity_id: int): return await db.get(Activity, activity_id)
