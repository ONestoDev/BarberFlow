import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.shared.database.enums import PaymentMethod


class PaymentCreate(BaseModel):
    method: PaymentMethod
    discount_amount: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2)
    notes: str | None = Field(default=None, max_length=2000)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    appointment_id: uuid.UUID
    created_by: uuid.UUID
    method: PaymentMethod
    original_amount: Decimal
    discount_amount: Decimal
    paid_amount: Decimal
    paid_at: datetime
    notes: str | None
    created_at: datetime
