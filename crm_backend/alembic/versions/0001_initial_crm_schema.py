"""create initial CRM schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-10-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = postgresql.ENUM("ADMIN", "SALES_REP", name="user_role")
    lead_source = postgresql.ENUM("WEBSITE", "REFERRAL", "LINKEDIN", "ADVERTISEMENT", "COLD_CALL", "OTHER", name="lead_source")
    lead_status = postgresql.ENUM("NEW", "CONTACTED", "QUALIFIED", "UNQUALIFIED", "CONVERTED", "LOST", name="lead_status")
    lead_priority = postgresql.ENUM("LOW", "MEDIUM", "HIGH", name="lead_priority")
    deal_stage = postgresql.ENUM("NEW", "QUALIFICATION", "PROPOSAL", "NEGOTIATION", "WON", "LOST", name="deal_stage")
    activity_type = postgresql.ENUM("CALL", "EMAIL", "MEETING", "NOTE", "FOLLOW_UP", name="activity_type")
    task_status = postgresql.ENUM("TODO", "IN_PROGRESS", "COMPLETED", "CANCELLED", name="task_status")
    task_priority = postgresql.ENUM("LOW", "MEDIUM", "HIGH", name="task_priority")
    for enum_type in [user_role, lead_source, lead_status, lead_priority, deal_stage, activity_type, task_status, task_priority]:
        enum_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("industry", sa.String(120)),
        sa.Column("website", sa.String(255)),
        sa.Column("phone", sa.String(30)),
        sa.Column("email", sa.String(255)),
        sa.Column("address", sa.String(500)),
        sa.Column("city", sa.String(100)),
        sa.Column("state", sa.String(100)),
        sa.Column("country", sa.String(100), server_default="India"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_companies_name", "companies", ["name"])
    op.create_index("ix_companies_email", "companies", ["email"])

    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(30)),
        sa.Column("designation", sa.String(120)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_contacts_company_id", "contacts", ["company_id"])
    op.create_index("ix_contacts_name", "contacts", ["name"])
    op.create_index("ix_contacts_email", "contacts", ["email"])

    op.create_table(
        "leads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(30)),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("contact_id", sa.Integer(), sa.ForeignKey("contacts.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("assigned_to", sa.Integer(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("source", lead_source, nullable=False),
        sa.Column("status", lead_status, nullable=False, server_default="NEW"),
        sa.Column("priority", lead_priority, nullable=False, server_default="MEDIUM"),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    for name,col in [("company_id","company_id"),("contact_id","contact_id"),("assigned_to","assigned_to"),("status","status"),("priority","priority")]: op.create_index(f"ix_leads_{name}","leads",[col])
    op.create_index("ix_leads_name","leads",["name"]); op.create_index("ix_leads_email","leads",["email"])

    op.create_table(
        "deals",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("contact_id", sa.Integer(), sa.ForeignKey("contacts.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("assigned_to", sa.Integer(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("value", sa.Numeric(14,2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default="INR"),
        sa.Column("stage", deal_stage, nullable=False, server_default="NEW"),
        sa.Column("probability", sa.Integer(), nullable=False, server_default="10"),
        sa.Column("expected_close_date", sa.Date()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_deals_title","deals",["title"]); op.create_index("ix_deals_company_id","deals",["company_id"]); op.create_index("ix_deals_contact_id","deals",["contact_id"]); op.create_index("ix_deals_assigned_to","deals",["assigned_to"]); op.create_index("ix_deals_stage","deals",["stage"])

    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("lead_id", sa.Integer(), sa.ForeignKey("leads.id", ondelete="CASCADE")),
        sa.Column("contact_id", sa.Integer(), sa.ForeignKey("contacts.id", ondelete="CASCADE")),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="CASCADE")),
        sa.Column("deal_id", sa.Integer(), sa.ForeignKey("deals.id", ondelete="CASCADE")),
        sa.Column("type", activity_type, nullable=False),
        sa.Column("subject", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("activity_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    for col in ["user_id","lead_id","contact_id","company_id","deal_id","type"]: op.create_index(f"ix_activities_{col}","activities",[col])

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("assigned_to", sa.Integer(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("lead_id", sa.Integer(), sa.ForeignKey("leads.id", ondelete="CASCADE")),
        sa.Column("contact_id", sa.Integer(), sa.ForeignKey("contacts.id", ondelete="CASCADE")),
        sa.Column("deal_id", sa.Integer(), sa.ForeignKey("deals.id", ondelete="CASCADE")),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("priority", task_priority, nullable=False, server_default="MEDIUM"),
        sa.Column("status", task_status, nullable=False, server_default="TODO"),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    for col in ["assigned_to","lead_id","contact_id","deal_id","priority","status","due_date"]: op.create_index(f"ix_tasks_{col}","tasks",[col])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("entity_type", sa.String(50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("old_data", sa.JSON()),
        sa.Column("new_data", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    for col in ["user_id","entity_type","entity_id"]: op.create_index(f"ix_audit_logs_{col}","audit_logs",[col])


def downgrade() -> None:
    for table in ["audit_logs","tasks","activities","deals","leads","contacts","companies","users"]:
        op.drop_table(table)
    for name in ["task_priority","task_status","activity_type","deal_stage","lead_priority","lead_status","lead_source","user_role"]:
        postgresql.ENUM(name=name).drop(op.get_bind(), checkfirst=True)
