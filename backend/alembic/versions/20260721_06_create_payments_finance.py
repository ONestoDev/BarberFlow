"""create payments and financial transactions

Revision ID: 20260721_06
Revises: 20260721_05
Create Date: 2026-07-21
"""

from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260721_06"
down_revision: str | None = "20260721_05"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    payment_method = sa.Enum("CASH", "PIX", "DEBIT_CARD", "CREDIT_CARD", name="payment_method")
    transaction_type = sa.Enum("INCOME", "EXPENSE", name="financial_transaction_type")
    origin_type = sa.Enum("APPOINTMENT", "SALE", "EXPENSE", "ADJUSTMENT", name="financial_origin_type")
    payment_method.create(op.get_bind(), checkfirst=True)
    transaction_type.create(op.get_bind(), checkfirst=True)
    origin_type.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("method", payment_method, nullable=False),
        sa.Column("original_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("discount_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("paid_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("original_amount >= 0", name="ck_payment_original_non_negative"),
        sa.CheckConstraint("discount_amount >= 0", name="ck_payment_discount_non_negative"),
        sa.CheckConstraint("paid_amount >= 0", name="ck_payment_paid_non_negative"),
        sa.CheckConstraint("original_amount = discount_amount + paid_amount", name="ck_payment_amount_composition"),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointments.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payments_appointment_id", "payments", ["appointment_id"], unique=True)
    op.create_table(
        "financial_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("transaction_type", transaction_type, nullable=False),
        sa.Column("origin_type", origin_type, nullable=False),
        sa.Column("origin_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("description", sa.String(length=240), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("amount > 0", name="ck_financial_transaction_amount_positive"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["payment_id"], ["payments.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    for column, unique in (("payment_id", True), ("transaction_type", False), ("origin_type", False), ("origin_id", False), ("occurred_at", False)):
        op.create_index(f"ix_financial_transactions_{column}", "financial_transactions", [column], unique=unique)


def downgrade() -> None:
    op.drop_table("financial_transactions")
    op.drop_table("payments")
    sa.Enum(name="financial_origin_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="financial_transaction_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="payment_method").drop(op.get_bind(), checkfirst=True)
