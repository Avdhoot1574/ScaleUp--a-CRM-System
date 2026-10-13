from decimal import Decimal
from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_leads: int
    qualified_leads: int
    total_contacts: int
    open_deals: int
    won_deals: int
    lost_deals: int
    total_pipeline_value: Decimal
    tasks_due_today: int
