import uuid
from datetime import datetime, timezone
from decimal import Decimal

from src.modules.finance.repository import FinanceRepository
from src.modules.finance.schemas import CashFlowSummary, CorrectionCreate, TransactionCreate
from src.modules.payments.models import FinancialTransaction
from src.shared.database.enums import FinancialOriginType, FinancialTransactionType


class TransactionNotFoundError(Exception): pass
class TransactionAlreadyCorrectedError(Exception): pass


class FinanceService:
    def __init__(self, repository: FinanceRepository): self.repository = repository

    def create(self, data: TransactionCreate, created_by: uuid.UUID):
        origin = (
            FinancialOriginType.EXPENSE
            if data.transaction_type == FinancialTransactionType.EXPENSE
            else FinancialOriginType.SALE
        )
        return self.repository.save(
            FinancialTransaction(
                created_by=created_by,
                transaction_type=data.transaction_type,
                origin_type=origin,
                amount=data.amount,
                category=data.category,
                description=data.description,
                occurred_at=data.occurred_at.astimezone(timezone.utc),
            )
        )

    def list(self, starts_at, ends_at, transaction_type=None):
        starts_at, ends_at = self._period(starts_at, ends_at)
        return self.repository.list(starts_at, ends_at, transaction_type)

    def summary(self, starts_at, ends_at):
        starts_at, ends_at = self._period(starts_at, ends_at)
        totals = self.repository.totals(starts_at, ends_at)
        income = totals.get(FinancialTransactionType.INCOME, Decimal("0.00"))
        expenses = totals.get(FinancialTransactionType.EXPENSE, Decimal("0.00"))
        return CashFlowSummary(
            starts_at=starts_at,
            ends_at=ends_at,
            income=income,
            expenses=expenses,
            profit=income - expenses,
        )

    def correct(self, transaction_id: uuid.UUID, data: CorrectionCreate, created_by: uuid.UUID):
        original = self.repository.get(transaction_id)
        if original is None:
            raise TransactionNotFoundError
        if original.correction_of_id is not None or self.repository.has_correction(transaction_id):
            raise TransactionAlreadyCorrectedError
        opposite = (
            FinancialTransactionType.EXPENSE
            if original.transaction_type == FinancialTransactionType.INCOME
            else FinancialTransactionType.INCOME
        )
        return self.repository.save(
            FinancialTransaction(
                created_by=created_by,
                transaction_type=opposite,
                origin_type=FinancialOriginType.ADJUSTMENT,
                origin_id=original.id,
                correction_of_id=original.id,
                amount=original.amount,
                category=original.category,
                description=f"Correção: {data.reason.strip()}",
                occurred_at=datetime.now(timezone.utc),
            )
        )

    @staticmethod
    def _period(starts_at, ends_at):
        if starts_at.tzinfo is None or ends_at.tzinfo is None or starts_at >= ends_at:
            raise ValueError("Período financeiro inválido.")
        return starts_at.astimezone(timezone.utc), ends_at.astimezone(timezone.utc)
