import uuid
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

from src.modules.appointments.models import Appointment, AppointmentService
from src.modules.appointments.repository import AppointmentRepository
from src.modules.appointments.schemas import (
    AppointmentCancel,
    AppointmentCreate,
    AppointmentReschedule,
    AppointmentStatusUpdate,
    AvailableSlot,
)
from src.shared.config.settings import settings
from src.shared.database.enums import AppointmentStatus


class AppointmentNotFoundError(Exception): pass
class InactiveReferenceError(Exception): pass
class InvalidServiceError(Exception): pass
class OutsideWorkingHoursError(Exception): pass
class ScheduleConflictError(Exception): pass
class InvalidAppointmentStateError(Exception): pass


class AppointmentServiceLayer:
    VALID_TRANSITIONS = {
        AppointmentStatus.SCHEDULED: {AppointmentStatus.CONFIRMED},
        AppointmentStatus.CONFIRMED: {AppointmentStatus.IN_PROGRESS},
        AppointmentStatus.IN_PROGRESS: {AppointmentStatus.COMPLETED},
        AppointmentStatus.COMPLETED: set(),
        AppointmentStatus.CANCELED: set(),
    }

    def __init__(self, repository: AppointmentRepository):
        self.repository = repository
        self.local_timezone = ZoneInfo(settings.app_timezone)

    def create(self, data: AppointmentCreate, created_by: uuid.UUID) -> Appointment:
        customer = self.repository.get_customer(data.customer_id)
        barber = self.repository.get_barber(data.barber_id)
        if customer is None or barber is None:
            raise InactiveReferenceError
        services = self.repository.get_services(data.service_ids)
        if len(services) != len(data.service_ids):
            raise InvalidServiceError
        services_by_id = {item.id: item for item in services}
        ordered_services = [services_by_id[item_id] for item_id in data.service_ids]
        starts_at = data.starts_at.astimezone(timezone.utc)
        ends_at = starts_at + timedelta(minutes=sum(item.duration_minutes for item in ordered_services))
        self._validate_availability(barber, starts_at, ends_at)
        appointment = Appointment(
            customer_id=data.customer_id,
            barber_id=data.barber_id,
            created_by=created_by,
            starts_at=starts_at,
            ends_at=ends_at,
            status=AppointmentStatus.SCHEDULED,
            notes=data.notes,
            services=[
                AppointmentService(
                    service_id=item.id,
                    service_name_at_time=item.name,
                    duration_at_time=item.duration_minutes,
                    price_at_time=item.price,
                )
                for item in ordered_services
            ],
        )
        return self.repository.save(appointment)

    def get(self, appointment_id: uuid.UUID) -> Appointment:
        appointment = self.repository.get(appointment_id)
        if appointment is None:
            raise AppointmentNotFoundError
        return appointment

    def list(self, starts_at: datetime, ends_at: datetime, barber_id: uuid.UUID | None):
        if starts_at.tzinfo is None or ends_at.tzinfo is None or starts_at >= ends_at:
            raise ValueError("Período de consulta inválido.")
        return self.repository.list(starts_at.astimezone(timezone.utc), ends_at.astimezone(timezone.utc), barber_id)

    def reschedule(self, appointment_id: uuid.UUID, data: AppointmentReschedule) -> Appointment:
        appointment = self.get(appointment_id)
        if appointment.status in {AppointmentStatus.CANCELED, AppointmentStatus.COMPLETED, AppointmentStatus.IN_PROGRESS}:
            raise InvalidAppointmentStateError
        barber = self.repository.get_barber(appointment.barber_id)
        if barber is None:
            raise InactiveReferenceError
        duration = appointment.ends_at - appointment.starts_at
        starts_at = data.starts_at.astimezone(timezone.utc)
        ends_at = starts_at + duration
        self._validate_availability(barber, starts_at, ends_at, appointment.id)
        appointment.starts_at = starts_at
        appointment.ends_at = ends_at
        return self.repository.save(appointment)

    def cancel(self, appointment_id: uuid.UUID, data: AppointmentCancel) -> Appointment:
        appointment = self.get(appointment_id)
        if appointment.status in {AppointmentStatus.CANCELED, AppointmentStatus.COMPLETED, AppointmentStatus.IN_PROGRESS}:
            raise InvalidAppointmentStateError
        appointment.status = AppointmentStatus.CANCELED
        appointment.cancellation_reason = data.reason.strip()
        return self.repository.save(appointment)

    def change_status(
        self,
        appointment_id: uuid.UUID,
        data: AppointmentStatusUpdate,
    ) -> Appointment:
        appointment = self.get(appointment_id)
        if data.status not in self.VALID_TRANSITIONS[appointment.status]:
            raise InvalidAppointmentStateError
        appointment.status = data.status
        return self.repository.save(appointment)

    def available_slots(
        self,
        barber_id: uuid.UUID,
        target_date: date,
        service_ids: list[uuid.UUID],
    ) -> list[AvailableSlot]:
        if not service_ids or len(set(service_ids)) != len(service_ids):
            raise InvalidServiceError
        barber = self.repository.get_barber(barber_id)
        if barber is None:
            raise InactiveReferenceError
        services = self.repository.get_services(service_ids)
        if len(services) != len(service_ids):
            raise InvalidServiceError
        schedule = next(
            (item for item in barber.schedules if item.weekday == target_date.weekday()),
            None,
        )
        if schedule is None:
            return []

        duration = timedelta(minutes=sum(item.duration_minutes for item in services))
        step = timedelta(minutes=settings.appointment_slot_interval_minutes)
        candidate = datetime.combine(target_date, schedule.start_time, self.local_timezone)
        work_end = datetime.combine(target_date, schedule.end_time, self.local_timezone)
        slots = []
        while candidate + duration <= work_end:
            candidate_end = candidate + duration
            start_utc = candidate.astimezone(timezone.utc)
            end_utc = candidate_end.astimezone(timezone.utc)
            overlaps_break = bool(
                schedule.break_start
                and candidate.time() < schedule.break_end
                and candidate_end.time() > schedule.break_start
            )
            if (
                not overlaps_break
                and not self.repository.has_unavailability(barber.id, start_utc, end_utc)
                and not self.repository.has_conflict(barber.id, start_utc, end_utc)
            ):
                slots.append(AvailableSlot(starts_at=candidate, ends_at=candidate_end))
            candidate += step
        return slots

    def _validate_availability(self, barber, starts_at, ends_at, exclude_id=None):
        local_start = starts_at.astimezone(self.local_timezone)
        local_end = ends_at.astimezone(self.local_timezone)
        if local_start.date() != local_end.date():
            raise OutsideWorkingHoursError
        schedule = next((item for item in barber.schedules if item.weekday == local_start.weekday()), None)
        start_time = local_start.replace(tzinfo=None).time()
        end_time = local_end.replace(tzinfo=None).time()
        if schedule is None or start_time < schedule.start_time or end_time > schedule.end_time:
            raise OutsideWorkingHoursError
        if schedule.break_start and start_time < schedule.break_end and end_time > schedule.break_start:
            raise OutsideWorkingHoursError
        if self.repository.has_unavailability(barber.id, starts_at, ends_at):
            raise ScheduleConflictError
        if self.repository.has_conflict(barber.id, starts_at, ends_at, exclude_id):
            raise ScheduleConflictError
