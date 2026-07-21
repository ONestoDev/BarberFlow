import uuid
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.modules.appointments.repository import AppointmentRepository
from src.modules.appointments.schemas import (
    AppointmentCancel,
    AppointmentCreate,
    AppointmentReschedule,
    AppointmentResponse,
    AppointmentStatusUpdate,
    AvailableSlot,
)
from src.modules.appointments.service import (
    AppointmentNotFoundError,
    AppointmentServiceLayer,
    InactiveReferenceError,
    InvalidAppointmentStateError,
    InvalidServiceError,
    OutsideWorkingHoursError,
    ScheduleConflictError,
)
from src.modules.auth.dependencies import require_roles
from src.modules.users.models import User
from src.shared.database.connection import get_db
from src.shared.database.enums import UserRole

router = APIRouter(prefix="/appointments", tags=["Agendamentos"])
staff_only = require_roles(UserRole.ADMIN, UserRole.BARBER)


def get_service(db: Session = Depends(get_db)):
    return AppointmentServiceLayer(AppointmentRepository(db))


def translate_error(exc):
    if isinstance(exc, AppointmentNotFoundError): return HTTPException(404, "Agendamento não encontrado.")
    if isinstance(exc, InvalidAppointmentStateError): return HTTPException(409, "O estado atual não permite esta operação.")
    if isinstance(exc, ScheduleConflictError): return HTTPException(409, "O barbeiro não está disponível neste horário.")
    if isinstance(exc, OutsideWorkingHoursError): return HTTPException(422, "O horário está fora da jornada do barbeiro.")
    if isinstance(exc, InvalidServiceError): return HTTPException(422, "Um ou mais serviços estão inativos ou não existem.")
    return HTTPException(422, "Cliente ou barbeiro inativo ou inexistente.")


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(data: AppointmentCreate, service=Depends(get_service), user: User = Depends(staff_only)):
    try: return service.create(data, user.id)
    except (InactiveReferenceError, InvalidServiceError, OutsideWorkingHoursError, ScheduleConflictError) as exc:
        raise translate_error(exc) from exc


@router.get("", response_model=list[AppointmentResponse])
def list_appointments(
    starts_at: datetime = Query(), ends_at: datetime = Query(), barber_id: uuid.UUID | None = None,
    service=Depends(get_service), _: User = Depends(staff_only),
):
    try: return service.list(starts_at, ends_at, barber_id)
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc


@router.get("/availability", response_model=list[AvailableSlot])
def get_availability(
    barber_id: uuid.UUID,
    date: date,
    service_ids: list[uuid.UUID] = Query(),
    service=Depends(get_service),
    _: User = Depends(staff_only),
):
    try:
        return service.available_slots(barber_id, date, service_ids)
    except (InactiveReferenceError, InvalidServiceError) as exc:
        raise translate_error(exc) from exc


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: uuid.UUID, service=Depends(get_service), _: User = Depends(staff_only)):
    try: return service.get(appointment_id)
    except AppointmentNotFoundError as exc: raise translate_error(exc) from exc


@router.patch("/{appointment_id}/reschedule", response_model=AppointmentResponse)
def reschedule_appointment(appointment_id: uuid.UUID, data: AppointmentReschedule, service=Depends(get_service), _: User = Depends(staff_only)):
    try: return service.reschedule(appointment_id, data)
    except (AppointmentNotFoundError, InvalidAppointmentStateError, InactiveReferenceError, OutsideWorkingHoursError, ScheduleConflictError) as exc:
        raise translate_error(exc) from exc


@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(appointment_id: uuid.UUID, data: AppointmentCancel, service=Depends(get_service), _: User = Depends(staff_only)):
    try: return service.cancel(appointment_id, data)
    except (AppointmentNotFoundError, InvalidAppointmentStateError) as exc: raise translate_error(exc) from exc


@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
def change_appointment_status(
    appointment_id: uuid.UUID,
    data: AppointmentStatusUpdate,
    service=Depends(get_service),
    _: User = Depends(staff_only),
):
    try:
        return service.change_status(appointment_id, data)
    except (AppointmentNotFoundError, InvalidAppointmentStateError) as exc:
        raise translate_error(exc) from exc
