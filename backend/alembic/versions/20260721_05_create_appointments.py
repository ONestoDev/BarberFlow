"""create appointments tables

Revision ID: 20260721_05
Revises: 20260721_04
Create Date: 2026-07-21
"""

from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260721_05"
down_revision: str | None = "20260721_04"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    appointment_status = sa.Enum("SCHEDULED", "CONFIRMED", "IN_PROGRESS", "COMPLETED", "CANCELED", name="appointment_status")
    appointment_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "appointments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("barber_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", appointment_status, nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("cancellation_reason", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("starts_at < ends_at", name="ck_appointment_range"),
        sa.ForeignKeyConstraint(["barber_id"], ["barbers.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in ("barber_id", "customer_id", "starts_at", "ends_at", "status"):
        op.create_index(f"ix_appointments_{column}", "appointments", [column])
    op.create_table(
        "appointment_services",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("service_name_at_time", sa.String(length=120), nullable=False),
        sa.Column("duration_at_time", sa.Integer(), nullable=False),
        sa.Column("price_at_time", sa.Numeric(10, 2), nullable=False),
        sa.CheckConstraint("duration_at_time > 0", name="ck_appointment_service_duration"),
        sa.CheckConstraint("price_at_time >= 0", name="ck_appointment_service_price"),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_appointment_services_appointment_id", "appointment_services", ["appointment_id"])
    op.create_index("ix_appointment_services_service_id", "appointment_services", ["service_id"])


def downgrade() -> None:
    op.drop_table("appointment_services")
    op.drop_table("appointments")
    sa.Enum(name="appointment_status").drop(op.get_bind(), checkfirst=True)
