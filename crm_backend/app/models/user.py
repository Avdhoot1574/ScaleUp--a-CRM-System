from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, Enum as SAEnum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SALES_REP = "SALES_REP"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True,)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, name="user_role"), default=UserRole.SALES_REP, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    assigned_leads = relationship("Lead", back_populates="assignee", foreign_keys="Lead.assigned_to")
    assigned_deals = relationship("Deal", back_populates="assignee", foreign_keys="Deal.assigned_to")
    tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to")
    activities = relationship("Activity", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
