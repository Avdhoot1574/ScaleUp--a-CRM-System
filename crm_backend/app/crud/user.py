from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

async def get_user(db: AsyncSession, user_id: int): return await db.get(User, user_id)
async def list_users(db: AsyncSession, offset: int, limit: int): return (await db.scalars(select(User).order_by(User.id.desc()).offset(offset).limit(limit))).all()
