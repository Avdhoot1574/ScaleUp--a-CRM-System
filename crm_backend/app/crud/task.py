from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task, TaskStatus

async def get_task(db: AsyncSession, task_id: int): return await db.get(Task, task_id)
async def list_tasks(db: AsyncSession, offset: int, limit: int, status=None, assigned_to=None):
    stmt=select(Task)
    if status: stmt=stmt.where(Task.status == status)
    if assigned_to: stmt=stmt.where(Task.assigned_to == assigned_to)
    return (await db.scalars(stmt.order_by(Task.due_date.asc()).offset(offset).limit(limit))).all()
