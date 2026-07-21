import uuid

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID

from src.shared.database.connection import Base
from src.shared.database.enums import FinancialOriginType, FinancialTransactionType, PaymentMethod
from src.shared.database.mixins import TimestampMixin


class Payment(Base, TimestampMixin):
    __tablename__ = "payments"
    __table_args__ = (
        CheckConstraint("original_amount >= 0", name="ck_payment_original_non_negative"),
        CheckConstraint("discount_amount >= 0", name="ck_payment_discount_non_negative"),
        CheckConstraint("paid_amount >= 0", name="ck_payment_paid_non_negative"),
        CheckConstraint(
            "original_amount = discount_amount + paid_amount",
            name="ck_payment_amount_composition",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("appointments.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
        index=True,
    )
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    method = Column(Enum(PaymentMethod, name="payment_method"), nullable=False)
    original_amount = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text, nullable=True)


class FinancialTransaction(Base, TimestampMixin):
    __tablename__ = "financial_transactions"
    __table_args__ = (CheckConstraint("amount > 0", name="ck_financial_transaction_amount_positive"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="RESTRICT"), nullable=True, unique=True, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    transaction_type = Column(Enum(FinancialTransactionType, name="financial_transaction_type"), nullable=False, index=True)
    origin_type = Column(Enum(FinancialOriginType, name="financial_origin_type"), nullable=False, index=True)
    origin_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    correction_of_id = Column(
        UUID(as_uuid=True),
        ForeignKey("financial_transactions.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )
    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(80), nullable=True, index=True)
    description = Column(String(240), nullable=False)
    occurred_at = Column(DateTime(timezone=True), nullable=False, index=True)
