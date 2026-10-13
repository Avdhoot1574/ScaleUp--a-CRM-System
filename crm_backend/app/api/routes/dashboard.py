from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import get_summary

router=APIRouter(prefix="/dashboard",tags=["Dashboard"])

@router.get("/summary",response_model=DashboardSummary)
async def summary(db:AsyncSession=Depends(get_db),_:User=Depends(get_current_user)):
    return await get_summary(db)
