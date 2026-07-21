import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.modules.payments.models import FinancialTransaction
from src.shared.database.enums import FinancialTransactionType


class FinanceRepository:
    def __init__(self, db: Session): self.db = db

    def get(self, transaction_id: uuid.UUID):
        return self.db.get(FinancialTransaction, transaction_id)

    def has_correction(self, transaction_id: uuid.UUID):
        statement = select(FinancialTransaction.id).where(
            FinancialTransaction.correction_of_id == transaction_id
        ).limit(1)
        return self.db.scalar(statement) is not None

    def list(self, starts_at: datetime, ends_at: datetime, transaction_type=None):
        statement = select(FinancialTransaction).where(
            FinancialTransaction.occurred_at >= starts_at,
            FinancialTransaction.occurred_at < ends_at,
        )
        if transaction_type:
            statement = statement.where(FinancialTransaction.transaction_type == transaction_type)
        return list(self.db.scalars(statement.order_by(FinancialTransaction.occurred_at)))

    def totals(self, starts_at: datetime, ends_at: datetime):
        statement = (
            select(FinancialTransaction.transaction_type, func.coalesce(func.sum(FinancialTransaction.amount), 0))
            .where(FinancialTransaction.occurred_at >= starts_at, FinancialTransaction.occurred_at < ends_at)
            .group_by(FinancialTransaction.transaction_type)
        )
        return {item_type: Decimal(str(total)) for item_type, total in self.db.execute(statement)}

    def save(self, transaction):
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
