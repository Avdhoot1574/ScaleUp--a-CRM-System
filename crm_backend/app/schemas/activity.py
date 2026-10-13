from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.activity import ActivityType

class ActivityCreate(BaseModel):
    lead_id: int | None = None
    contact_id: int | None = None
    company_id: int | None = None
    deal_id: int | None = None
    type: ActivityType
    subject: str = Field(min_length=1, max_length=200)
    description: str | None = None
    activity_time: datetime

    @model_validator(mode="after")
    def exactly_one_target(self):
        if sum(value is not None for value in [self.lead_id, self.contact_id, self.company_id, self.deal_id]) != 1:
            raise ValueError("Exactly one target is required: lead_id, contact_id, company_id, or deal_id")
        return self

class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    lead_id: int | None
    contact_id: int | None
    company_id: int | None
    deal_id: int | None
    type: ActivityType
    subject: str
    description: str | None
    activity_time: datetime
    created_at: datetime
