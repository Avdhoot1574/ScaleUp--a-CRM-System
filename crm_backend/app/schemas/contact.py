from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ContactCreate(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr | None = None
    phone: str | None = None
    designation: str | None = None

class ContactUpdate(BaseModel):
    company_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=200)
    email: EmailStr | None = None
    phone: str | None = None
    designation: str | None = None

class ContactResponse(ContactCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
