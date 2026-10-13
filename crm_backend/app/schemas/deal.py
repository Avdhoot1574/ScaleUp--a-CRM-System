from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.models.deal import DealStage

class DealCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    company_id: int
    contact_id: int
    assigned_to: int
    value: Decimal = Field(ge=0, decimal_places=2)
    stage: DealStage = DealStage.NEW
    probability: int | None = Field(default=None, ge=0, le=100)
    expected_close_date: date | None = None

class DealUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    company_id: int | None = None
    contact_id: int | None = None
    assigned_to: int | None = None
    value: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    stage: DealStage | None = None
    probability: int | None = Field(default=None, ge=0, le=100)
    expected_close_date: date | None = None

class DealResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: str | None
    company_id: int
    contact_id: int
    assigned_to: int
    value: Decimal
    currency: str
    stage: DealStage
    probability: int
    expected_close_date: date | None
    created_at: datetime
    updated_at: datetime
