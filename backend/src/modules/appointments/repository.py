import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.appointments.models import Appointment
from src.modules.barbers.models import Barber, BarberUnavailability
from src.modules.customers.models import Customer
from src.modules.services.models import Service
from src.shared.database.enums import AppointmentStatus


class AppointmentRepository:
    def __init__(self, db: Session): self.db = db

    def get_customer(self, customer_id):
        return self.db.scalar(select(Customer).where(Customer.id == customer_id, Customer.active.is_(True)))

    def get_barber(self, barber_id):
        return self.db.scalar(select(Barber).where(Barber.id == barber_id, Barber.active.is_(True)))

    def get_services(self, service_ids):
        return list(self.db.scalars(select(Service).where(Service.id.in_(service_ids), Service.active.is_(True))))

    def get(self, appointment_id):
        return self.db.get(Appointment, appointment_id)

    def list(self, starts_at: datetime, ends_at: datetime, barber_id: uuid.UUID | None):
        statement = select(Appointment).where(Appointment.starts_at < ends_at, Appointment.ends_at > starts_at)
        if barber_id:
            statement = statement.where(Appointment.barber_id == barber_id)
        return list(self.db.scalars(statement.order_by(Appointment.starts_at)))

    def has_conflict(self, barber_id, starts_at, ends_at, exclude_id=None):
        statement = select(Appointment.id).where(
            Appointment.barber_id == barber_id,
            Appointment.status != AppointmentStatus.CANCELED,
            Appointment.starts_at < ends_at,
            Appointment.ends_at > starts_at,
        )
        if exclude_id:
            statement = statement.where(Appointment.id != exclude_id)
        return self.db.scalar(statement.limit(1)) is not None

    def has_unavailability(self, barber_id, starts_at, ends_at):
        statement = select(BarberUnavailability.id).where(
            BarberUnavailability.barber_id == barber_id,
            BarberUnavailability.starts_at < ends_at,
            BarberUnavailability.ends_at > starts_at,
        )
        return self.db.scalar(statement.limit(1)) is not None

    def save(self, appointment):
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
