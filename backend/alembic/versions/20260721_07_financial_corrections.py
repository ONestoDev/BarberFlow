"""add financial categories and corrections

Revision ID: 20260721_07
Revises: 20260721_06
Create Date: 2026-07-21
"""

from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260721_07"
down_revision: str | None = "20260721_06"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("financial_transactions", sa.Column("correction_of_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("financial_transactions", sa.Column("category", sa.String(length=80), nullable=True))
    op.create_foreign_key(
        "fk_financial_transactions_correction_of_id",
        "financial_transactions",
        "financial_transactions",
        ["correction_of_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_index("ix_financial_transactions_correction_of_id", "financial_transactions", ["correction_of_id"])
    op.create_index("ix_financial_transactions_category", "financial_transactions", ["category"])


def downgrade() -> None:
    op.drop_index("ix_financial_transactions_category", table_name="financial_transactions")
    op.drop_index("ix_financial_transactions_correction_of_id", table_name="financial_transactions")
    op.drop_constraint("fk_financial_transactions_correction_of_id", "financial_transactions", type_="foreignkey")
    op.drop_column("financial_transactions", "category")
    op.drop_column("financial_transactions", "correction_of_id")
