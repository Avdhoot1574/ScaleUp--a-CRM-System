from datetime import datetime
from enum import Enum
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import inspect
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    old_data: Mapped[dict | None] = mapped_column(JSON)
    new_data: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="audit_logs")


def _json_value(value):
    if isinstance(value, (datetime, Decimal, Enum)):
        return value.value if isinstance(value, Enum) else str(value)
    return value


def _snapshot(obj):
    if isinstance(obj, (AuditLog,)):
        return None
    mapper = inspect(obj).mapper
    result = {}
    for column in mapper.columns:
        if column.name == "password_hash":
            continue
        result[column.name] = _json_value(getattr(obj, column.name, None))
    return result


@event.listens_for(Session, "after_flush")
def create_audit_logs(session: Session, flush_context):
    user_id = session.info.get("user_id")
    if not user_id:
        return

    pending = []
    for obj in list(session.new):
        if isinstance(obj, AuditLog) or not hasattr(obj, "id") or obj.__class__.__name__ == "User":
            continue
        pending.append(AuditLog(user_id=user_id, entity_type=obj.__class__.__name__, entity_id=obj.id, action="CREATE", new_data=_snapshot(obj)))

    for obj in list(session.dirty):
        if isinstance(obj, AuditLog) or not hasattr(obj, "id") or obj.__class__.__name__ == "User":
            continue
        if session.is_modified(obj, include_collections=False):
            pending.append(AuditLog(user_id=user_id, entity_type=obj.__class__.__name__, entity_id=obj.id, action="UPDATE", new_data=_snapshot(obj)))

    for obj in list(session.deleted):
        if isinstance(obj, AuditLog) or not hasattr(obj, "id") or obj.__class__.__name__ == "User":
            continue
        pending.append(AuditLog(user_id=user_id, entity_type=obj.__class__.__name__, entity_id=obj.id, action="DELETE", old_data=_snapshot(obj)))

    session.add_all(pending)
