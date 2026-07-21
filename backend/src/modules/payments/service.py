import uuid
from datetime import datetime, timezone
from decimal import Decimal

from src.modules.payments.models import FinancialTransaction, Payment
from src.modules.payments.repository import DuplicatePaymentError, PaymentRepository
from src.modules.payments.schemas import PaymentCreate
from src.shared.database.enums import AppointmentStatus, FinancialOriginType, FinancialTransactionType


class PayableAppointmentNotFoundError(Exception): pass
class AppointmentAlreadyPaidError(Exception): pass
class InvalidDiscountError(Exception): pass
class ZeroValuePaymentError(Exception): pass


class PaymentService:
    def __init__(self, repository: PaymentRepository): self.repository = repository

    def create(self, appointment_id: uuid.UUID, data: PaymentCreate, created_by: uuid.UUID) -> Payment:
        appointment = self.repository.get_appointment(appointment_id)
        if appointment is None or appointment.status == AppointmentStatus.CANCELED:
            raise PayableAppointmentNotFoundError
        if self.repository.get_by_appointment(appointment_id) is not None:
            raise AppointmentAlreadyPaidError
        original_amount = sum(
            (item.price_at_time for item in appointment.services),
            start=Decimal("0.00"),
        )
        if data.discount_amount > original_amount:
            raise InvalidDiscountError
        paid_amount = original_amount - data.discount_amount
        if paid_amount <= 0:
            raise ZeroValuePaymentError
        now = datetime.now(timezone.utc)
        payment_id = uuid.uuid4()
        payment = Payment(
            id=payment_id,
            appointment_id=appointment_id,
            created_by=created_by,
            method=data.method,
            original_amount=original_amount,
            discount_amount=data.discount_amount,
            paid_amount=paid_amount,
            paid_at=now,
            notes=data.notes,
        )
        transaction = FinancialTransaction(
            payment_id=payment_id,
            created_by=created_by,
            transaction_type=FinancialTransactionType.INCOME,
            origin_type=FinancialOriginType.APPOINTMENT,
            origin_id=appointment_id,
            amount=paid_amount,
            description="Pagamento de atendimento",
            occurred_at=now,
        )
        try:
            return self.repository.save_with_transaction(payment, transaction)
        except DuplicatePaymentError as exc:
            raise AppointmentAlreadyPaidError from exc

    def get_by_appointment(self, appointment_id: uuid.UUID) -> Payment:
        payment = self.repository.get_by_appointment(appointment_id)
        if payment is None:
            raise PayableAppointmentNotFoundError
        return payment
