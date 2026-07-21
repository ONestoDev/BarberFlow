import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.modules.finance.schemas import CorrectionCreate, TransactionCreate
from src.modules.finance.service import FinanceService, TransactionAlreadyCorrectedError, TransactionNotFoundError
from src.modules.payments.models import FinancialTransaction
from src.shared.database.enums import FinancialOriginType, FinancialTransactionType


class FakeRepository:
    def __init__(self, original=None, corrected=False):
        self.original = original
        self.corrected = corrected
        self.saved = []
        self.values = {
            FinancialTransactionType.INCOME: Decimal("1000.00"),
            FinancialTransactionType.EXPENSE: Decimal("350.00"),
        }
    def get(self, transaction_id): return self.original
    def has_correction(self, transaction_id): return self.corrected
    def list(self, *args): return self.saved
    def totals(self, *args): return self.values
    def save(self, transaction): self.saved.append(transaction); return transaction


def period():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    return start, start + timedelta(days=31)


def test_expense_requires_category():
    with pytest.raises(ValidationError):
        TransactionCreate(
            transaction_type=FinancialTransactionType.EXPENSE,
            amount=Decimal("100"),
            description="Energia",
            occurred_at=period()[0],
        )


def test_create_expense_preserves_category_and_origin():
    repository = FakeRepository()
    data = TransactionCreate(
        transaction_type=FinancialTransactionType.EXPENSE,
        amount=Decimal("150.50"),
        description=" Conta de energia ",
        category=" Contas fixas ",
        occurred_at=period()[0],
    )
    result = FinanceService(repository).create(data, uuid.uuid4())
    assert result.origin_type == FinancialOriginType.EXPENSE
    assert result.category == "Contas fixas"
    assert result.description == "Conta de energia"


def test_summary_calculates_profit():
    summary = FinanceService(FakeRepository()).summary(*period())
    assert summary.income == Decimal("1000.00")
    assert summary.expenses == Decimal("350.00")
    assert summary.profit == Decimal("650.00")


def test_correction_creates_opposite_transaction():
    original = FinancialTransaction(
        id=uuid.uuid4(),
        transaction_type=FinancialTransactionType.INCOME,
        amount=Decimal("80.00"),
        category=None,
        correction_of_id=None,
    )
    result = FinanceService(FakeRepository(original=original)).correct(
        original.id, CorrectionCreate(reason="Lançamento duplicado"), uuid.uuid4()
    )
    assert result.transaction_type == FinancialTransactionType.EXPENSE
    assert result.origin_type == FinancialOriginType.ADJUSTMENT
    assert result.correction_of_id == original.id
    assert result.amount == original.amount


def test_transaction_cannot_be_corrected_twice():
    original = FinancialTransaction(id=uuid.uuid4(), correction_of_id=None)
    with pytest.raises(TransactionAlreadyCorrectedError):
        FinanceService(FakeRepository(original=original, corrected=True)).correct(
            original.id, CorrectionCreate(reason="Outra correção"), uuid.uuid4()
        )


def test_unknown_transaction_cannot_be_corrected():
    with pytest.raises(TransactionNotFoundError):
        FinanceService(FakeRepository()).correct(
            uuid.uuid4(), CorrectionCreate(reason="Correção"), uuid.uuid4()
        )
