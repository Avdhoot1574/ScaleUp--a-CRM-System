from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.task import TaskPriority, TaskStatus

class TaskCreate(BaseModel):
    assigned_to: int
    lead_id: int | None = None
    contact_id: int | None = None
    deal_id: int | None = None
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.TODO
    due_date: date

    @model_validator(mode="after")
    def at_least_one_target(self):
        if not any(value is not None for value in [self.lead_id, self.contact_id, self.deal_id]):
            raise ValueError("At least one target is required: lead_id, contact_id, or deal_id")
        return self

class TaskUpdate(BaseModel):
    assigned_to: int | None = None
    lead_id: int | None = None
    contact_id: int | None = None
    deal_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    priority: TaskPriority | None = None
    status: TaskStatus | None = None
    due_date: date | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    assigned_to: int
    lead_id: int | None
    contact_id: int | None
    deal_id: int | None
    title: str
    description: str | None
    priority: TaskPriority
    status: TaskStatus
    due_date: date
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
