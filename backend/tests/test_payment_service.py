import uuid
from decimal import Decimal

import pytest

from src.modules.appointments.models import Appointment, AppointmentService
from src.modules.payments.repository import DuplicatePaymentError
from src.modules.payments.schemas import PaymentCreate
from src.modules.payments.service import (
    AppointmentAlreadyPaidError,
    InvalidDiscountError,
    PayableAppointmentNotFoundError,
    PaymentService,
    ZeroValuePaymentError,
)
from src.shared.database.enums import AppointmentStatus, FinancialOriginType, FinancialTransactionType, PaymentMethod


class FakeRepository:
    def __init__(self, appointment=None, existing=None, duplicate=False):
        self.appointment = appointment
        self.existing = existing
        self.duplicate = duplicate
        self.transaction = None

    def get_appointment(self, appointment_id): return self.appointment
    def get_by_appointment(self, appointment_id): return self.existing
    def save_with_transaction(self, payment, transaction):
        if self.duplicate: raise DuplicatePaymentError
        self.existing = payment
        self.transaction = transaction
        return payment


def appointment(status=AppointmentStatus.SCHEDULED):
    return Appointment(
        id=uuid.uuid4(),
        status=status,
        services=[
            AppointmentService(price_at_time=Decimal("40.00")),
            AppointmentService(price_at_time=Decimal("25.00")),
        ],
    )


def test_payment_uses_snapshot_total_and_creates_income():
    item = appointment()
    repository = FakeRepository(appointment=item)
    payment = PaymentService(repository).create(
        item.id,
        PaymentCreate(method=PaymentMethod.PIX, discount_amount=Decimal("5.00")),
        uuid.uuid4(),
    )
    assert payment.original_amount == Decimal("65.00")
    assert payment.discount_amount == Decimal("5.00")
    assert payment.paid_amount == Decimal("60.00")
    assert repository.transaction.amount == Decimal("60.00")
    assert repository.transaction.transaction_type == FinancialTransactionType.INCOME
    assert repository.transaction.origin_type == FinancialOriginType.APPOINTMENT
    assert repository.transaction.payment_id == payment.id


def test_payment_rejects_discount_above_total():
    item = appointment()
    with pytest.raises(InvalidDiscountError):
        PaymentService(FakeRepository(appointment=item)).create(
            item.id, PaymentCreate(method=PaymentMethod.CASH, discount_amount=Decimal("70")), uuid.uuid4()
        )


def test_payment_rejects_zero_final_value():
    item = appointment()
    with pytest.raises(ZeroValuePaymentError):
        PaymentService(FakeRepository(appointment=item)).create(
            item.id, PaymentCreate(method=PaymentMethod.CASH, discount_amount=Decimal("65")), uuid.uuid4()
        )


def test_canceled_appointment_cannot_be_paid():
    item = appointment(AppointmentStatus.CANCELED)
    with pytest.raises(PayableAppointmentNotFoundError):
        PaymentService(FakeRepository(appointment=item)).create(
            item.id, PaymentCreate(method=PaymentMethod.PIX), uuid.uuid4()
        )


def test_appointment_cannot_have_two_payments():
    item = appointment()
    with pytest.raises(AppointmentAlreadyPaidError):
        PaymentService(FakeRepository(appointment=item, existing=object())).create(
            item.id, PaymentCreate(method=PaymentMethod.PIX), uuid.uuid4()
        )


def test_unique_constraint_race_is_translated():
    item = appointment()
    with pytest.raises(AppointmentAlreadyPaidError):
        PaymentService(FakeRepository(appointment=item, duplicate=True)).create(
            item.id, PaymentCreate(method=PaymentMethod.PIX), uuid.uuid4()
        )
