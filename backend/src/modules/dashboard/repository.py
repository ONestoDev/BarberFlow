from datetime import datetime
from decimal import Decimal

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from src.modules.appointments.models import Appointment, AppointmentService
from src.modules.barbers.models import Barber
from src.modules.customers.models import Customer
from src.modules.payments.models import Payment
from src.modules.users.models import User
from src.shared.database.enums import AppointmentStatus


class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def revenue(self, starts_at: datetime, ends_at: datetime) -> Decimal:
        statement = select(func.coalesce(func.sum(Payment.paid_amount), 0)).where(
            Payment.paid_at >= starts_at,
            Payment.paid_at < ends_at,
        )
        return Decimal(str(self.db.scalar(statement)))

    def completed_appointments(self, starts_at: datetime, ends_at: datetime) -> int:
        statement = select(func.count(Appointment.id)).where(
            Appointment.status == AppointmentStatus.COMPLETED,
            Appointment.ends_at >= starts_at,
            Appointment.ends_at < ends_at,
        )
        return int(self.db.scalar(statement) or 0)

    def new_customers(self, starts_at: datetime, ends_at: datetime) -> int:
        statement = select(func.count(Customer.id)).where(
            Customer.created_at >= starts_at,
            Customer.created_at < ends_at,
        )
        return int(self.db.scalar(statement) or 0)

    def top_services(self, starts_at: datetime, ends_at: datetime, limit: int = 5):
        quantity = func.count(AppointmentService.id).label("quantity")
        statement = (
            select(
                AppointmentService.service_id,
                AppointmentService.service_name_at_time,
                quantity,
            )
            .join(Appointment, Appointment.id == AppointmentService.appointment_id)
            .where(
                Appointment.status == AppointmentStatus.COMPLETED,
                Appointment.ends_at >= starts_at,
                Appointment.ends_at < ends_at,
            )
            .group_by(
                AppointmentService.service_id,
                AppointmentService.service_name_at_time,
            )
            .order_by(desc(quantity), AppointmentService.service_name_at_time)
            .limit(limit)
        )
        return list(self.db.execute(statement))

    def top_barber(self, starts_at: datetime, ends_at: datetime):
        revenue = func.sum(Payment.paid_amount).label("revenue")
        statement = (
            select(Barber.id, User.name, revenue)
            .join(Appointment, Appointment.barber_id == Barber.id)
            .join(Payment, Payment.appointment_id == Appointment.id)
            .join(User, User.id == Barber.user_id)
            .where(Payment.paid_at >= starts_at, Payment.paid_at < ends_at)
            .group_by(Barber.id, User.name)
            .order_by(desc(revenue), User.name)
            .limit(1)
        )
        return self.db.execute(statement).first()
