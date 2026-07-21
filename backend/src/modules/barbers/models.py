import uuid

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text, Time, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.shared.database.connection import Base
from src.shared.database.mixins import SoftDeleteMixin, TimestampMixin


class Barber(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "barbers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    bio = Column(Text, nullable=True)

    specialties = relationship("BarberSpecialty", cascade="all, delete-orphan", lazy="selectin")
    schedules = relationship("BarberSchedule", cascade="all, delete-orphan", lazy="selectin")


class BarberSpecialty(Base):
    __tablename__ = "barber_specialties"
    __table_args__ = (UniqueConstraint("barber_id", "name", name="uq_barber_specialty_name"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(80), nullable=False)


class BarberSchedule(Base):
    __tablename__ = "barber_schedules"
    __table_args__ = (
        UniqueConstraint("barber_id", "weekday", name="uq_barber_schedule_weekday"),
        CheckConstraint("weekday BETWEEN 0 AND 6", name="ck_barber_schedule_weekday"),
        CheckConstraint("start_time < end_time", name="ck_barber_schedule_range"),
        CheckConstraint(
            "(break_start IS NULL AND break_end IS NULL) OR "
            "(break_start IS NOT NULL AND break_end IS NOT NULL AND "
            "start_time < break_start AND break_start < break_end AND break_end < end_time)",
            name="ck_barber_schedule_break",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id", ondelete="CASCADE"), nullable=False, index=True)
    weekday = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    break_start = Column(Time, nullable=True)
    break_end = Column(Time, nullable=True)


class BarberUnavailability(Base, TimestampMixin):
    __tablename__ = "barber_unavailabilities"
    __table_args__ = (CheckConstraint("starts_at < ends_at", name="ck_barber_unavailability_range"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barber_id = Column(UUID(as_uuid=True), ForeignKey("barbers.id", ondelete="CASCADE"), nullable=False, index=True)
    starts_at = Column(DateTime(timezone=True), nullable=False, index=True)
    ends_at = Column(DateTime(timezone=True), nullable=False, index=True)
    reason = Column(String(240), nullable=True)
