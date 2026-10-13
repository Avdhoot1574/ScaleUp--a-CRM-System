from datetime import date
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact import Contact
from app.models.deal import Deal, DealStage
from app.models.lead import Lead, LeadStatus
from app.models.task import Task, TaskStatus
from app.schemas.dashboard import DashboardSummary

async def get_summary(db: AsyncSession) -> DashboardSummary:
    total_leads = await db.scalar(select(func.count(Lead.id))) or 0
    qualified = await db.scalar(select(func.count(Lead.id)).where(Lead.status == LeadStatus.QUALIFIED)) or 0
    contacts = await db.scalar(select(func.count(Contact.id))) or 0
    open_deals = await db.scalar(select(func.count(Deal.id)).where(Deal.stage.notin_([DealStage.WON, DealStage.LOST]))) or 0
    won = await db.scalar(select(func.count(Deal.id)).where(Deal.stage == DealStage.WON)) or 0
    lost = await db.scalar(select(func.count(Deal.id)).where(Deal.stage == DealStage.LOST)) or 0
    pipeline = await db.scalar(select(func.coalesce(func.sum(Deal.value), 0)).where(Deal.stage.notin_([DealStage.WON, DealStage.LOST]))) or Decimal("0")
    due_today = await db.scalar(select(func.count(Task.id)).where(Task.due_date == date.today(), Task.status.notin_([TaskStatus.COMPLETED, TaskStatus.CANCELLED]))) or 0
    return DashboardSummary(total_leads=total_leads, qualified_leads=qualified, total_contacts=contacts, open_deals=open_deals, won_deals=won, lost_deals=lost, total_pipeline_value=pipeline, tasks_due_today=due_today)
