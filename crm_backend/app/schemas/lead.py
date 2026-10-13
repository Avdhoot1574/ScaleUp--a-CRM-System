from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.lead import LeadPriority, LeadSource, LeadStatus

class LeadCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: str | None = None
    phone: str | None = None
    company_id: int
    contact_id: int
    assigned_to: int
    source: LeadSource
    status: LeadStatus = LeadStatus.NEW
    priority: LeadPriority = LeadPriority.MEDIUM
    notes: str | None = None

class LeadUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    email: str | None = None
    phone: str | None = None
    company_id: int | None = None
    contact_id: int | None = None
    assigned_to: int | None = None
    source: LeadSource | None = None
    status: LeadStatus | None = None
    priority: LeadPriority | None = None
    notes: str | None = None

class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str | None
    phone: str | None
    company_id: int
    contact_id: int
    assigned_to: int
    source: LeadSource
    status: LeadStatus
    priority: LeadPriority
    notes: str | None
    created_at: datetime
    updated_at: datetime

class LeadConversionResponse(BaseModel):
    lead: LeadResponse
    deal_id: int
