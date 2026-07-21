import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.modules.appointments.models import Appointment
from src.modules.payments.models import FinancialTransaction, Payment


class DuplicatePaymentError(Exception): pass


class PaymentRepository:
    def __init__(self, db: Session): self.db = db

    def get_appointment(self, appointment_id: uuid.UUID):
        return self.db.get(Appointment, appointment_id)

    def get_by_appointment(self, appointment_id: uuid.UUID):
        return self.db.scalar(select(Payment).where(Payment.appointment_id == appointment_id))

    def save_with_transaction(self, payment: Payment, transaction: FinancialTransaction):
        self.db.add_all([payment, transaction])
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise DuplicatePaymentError from exc
        self.db.refresh(payment)
        return payment
