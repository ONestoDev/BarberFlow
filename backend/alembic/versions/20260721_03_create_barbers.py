"""create barbers and availability tables

Revision ID: 20260721_03
Revises: 20260721_02
Create Date: 2026-07-21
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260721_03"
down_revision: str | None = "20260721_02"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "barbers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_barbers_user_id", "barbers", ["user_id"], unique=True)

    op.create_table(
        "barber_specialties",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("barber_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.ForeignKeyConstraint(["barber_id"], ["barbers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("barber_id", "name", name="uq_barber_specialty_name"),
    )
    op.create_index("ix_barber_specialties_barber_id", "barber_specialties", ["barber_id"])

    op.create_table(
        "barber_schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("barber_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("break_start", sa.Time(), nullable=True),
        sa.Column("break_end", sa.Time(), nullable=True),
        sa.CheckConstraint("weekday BETWEEN 0 AND 6", name="ck_barber_schedule_weekday"),
        sa.CheckConstraint("start_time < end_time", name="ck_barber_schedule_range"),
        sa.CheckConstraint(
            "(break_start IS NULL AND break_end IS NULL) OR "
            "(break_start IS NOT NULL AND break_end IS NOT NULL AND "
            "start_time < break_start AND break_start < break_end AND break_end < end_time)",
            name="ck_barber_schedule_break",
        ),
        sa.ForeignKeyConstraint(["barber_id"], ["barbers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("barber_id", "weekday", name="uq_barber_schedule_weekday"),
    )
    op.create_index("ix_barber_schedules_barber_id", "barber_schedules", ["barber_id"])

    op.create_table(
        "barber_unavailabilities",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("barber_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.String(length=240), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("starts_at < ends_at", name="ck_barber_unavailability_range"),
        sa.ForeignKeyConstraint(["barber_id"], ["barbers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_barber_unavailabilities_barber_id", "barber_unavailabilities", ["barber_id"])
    op.create_index("ix_barber_unavailabilities_starts_at", "barber_unavailabilities", ["starts_at"])
    op.create_index("ix_barber_unavailabilities_ends_at", "barber_unavailabilities", ["ends_at"])


def downgrade() -> None:
    op.drop_table("barber_unavailabilities")
    op.drop_table("barber_schedules")
    op.drop_table("barber_specialties")
    op.drop_index("ix_barbers_user_id", table_name="barbers")
    op.drop_table("barbers")
