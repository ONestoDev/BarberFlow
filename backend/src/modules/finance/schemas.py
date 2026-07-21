import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from src.shared.database.enums import FinancialTransactionType


class TransactionCreate(BaseModel):
    transaction_type: FinancialTransactionType
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    description: str = Field(min_length=2, max_length=240)
    category: str | None = Field(default=None, max_length=80)
    occurred_at: datetime

    @field_validator("occurred_at")
    @classmethod
    def aware_datetime(cls, value):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("A data deve possuir fuso horário.")
        return value

    @model_validator(mode="after")
    def expense_requires_category(self):
        if self.transaction_type == FinancialTransactionType.EXPENSE and not (
            self.category and self.category.strip()
        ):
            raise ValueError("Toda saída deve possuir categoria.")
        if self.category:
            self.category = " ".join(self.category.split())
        self.description = " ".join(self.description.split())
        return self


class CorrectionCreate(BaseModel):
    reason: str = Field(min_length=2, max_length=220)


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    payment_id: uuid.UUID | None
    correction_of_id: uuid.UUID | None
    created_by: uuid.UUID
    transaction_type: FinancialTransactionType
    origin_type: str
    origin_id: uuid.UUID | None
    amount: Decimal
    category: str | None
    description: str
    occurred_at: datetime
    created_at: datetime


class CashFlowSummary(BaseModel):
    starts_at: datetime
    ends_at: datetime
    income: Decimal
    expenses: Decimal
    profit: Decimal
