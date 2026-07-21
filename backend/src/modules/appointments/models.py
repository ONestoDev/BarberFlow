import uuid

from sqlalchemy import CheckConstraint, Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.shared.database.connection import Base
from src.shared.database.enums import AppointmentStatus
from src.shared.database.mixins import TimestampMixin


class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"
    __table_args__ = (CheckConstraint("starts_at < ends_at", name="ck_appointment_range"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False, index=True)
    barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id", ondelete="RESTRICT"), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    starts_at = Column(DateTime(timezone=True), nullable=False, index=True)
    ends_at = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(Enum(AppointmentStatus, name="appointment_status"), nullable=False, index=True)
    notes = Column(Text, nullable=True)
    cancellation_reason = Column(String(500), nullable=True)

    services = relationship("AppointmentService", cascade="all, delete-orphan", lazy="selectin")


class AppointmentService(Base):
    __tablename__ = "appointment_services"
    __table_args__ = (
        CheckConstraint("duration_at_time > 0", name="ck_appointment_service_duration"),
        CheckConstraint("price_at_time >= 0", name="ck_appointment_service_price"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    appointment_id = Column(UUID(as_uuid=True), ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False, index=True)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id", ondelete="RESTRICT"), nullable=False, index=True)
    service_name_at_time = Column(String(120), nullable=False)
    duration_at_time = Column(Integer, nullable=False)
    price_at_time = Column(Numeric(10, 2), nullable=False)
