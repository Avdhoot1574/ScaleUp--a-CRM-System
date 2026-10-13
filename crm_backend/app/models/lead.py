from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class LeadStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    UNQUALIFIED = "UNQUALIFIED"
    CONVERTED = "CONVERTED"
    LOST = "LOST"

class LeadPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class LeadSource(str, Enum):
    WEBSITE = "WEBSITE"
    REFERRAL = "REFERRAL"
    LINKEDIN = "LINKEDIN"
    ADVERTISEMENT = "ADVERTISEMENT"
    COLD_CALL = "COLD_CALL"
    OTHER = "OTHER"

class Lead(Base):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    email: Mapped[str | None] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(30))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False, index=True)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id", ondelete="RESTRICT"), nullable=False, index=True)
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    source: Mapped[LeadSource] = mapped_column(SAEnum(LeadSource, name="lead_source"), nullable=False)
    status: Mapped[LeadStatus] = mapped_column(SAEnum(LeadStatus, name="lead_status"), default=LeadStatus.NEW, nullable=False, index=True)
    priority: Mapped[LeadPriority] = mapped_column(SAEnum(LeadPriority, name="lead_priority"), default=LeadPriority.MEDIUM, nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="leads")
    contact = relationship("Contact", back_populates="leads")
    assignee = relationship("User", back_populates="assigned_leads", foreign_keys=[assigned_to])
    activities = relationship("Activity", back_populates="lead")
    tasks = relationship("Task", back_populates="lead")
