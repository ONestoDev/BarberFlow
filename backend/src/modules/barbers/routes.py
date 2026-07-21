import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.modules.auth.dependencies import require_roles
from src.modules.barbers.repository import BarberRepository
from src.modules.barbers.schemas import (
    BarberCreate,
    BarberResponse,
    BarberUpdate,
    UnavailabilityCreate,
    UnavailabilityResponse,
)
from src.modules.barbers.service import (
    BarberNotFoundError,
    BarberService,
    InvalidBarberUserError,
    UserAlreadyLinkedError,
)
from src.modules.users.models import User
from src.shared.database.connection import get_db
from src.shared.database.enums import UserRole

router = APIRouter(prefix="/barbers", tags=["Barbeiros"])
admin_only = require_roles(UserRole.ADMIN)
staff_only = require_roles(UserRole.ADMIN, UserRole.BARBER)


def get_service(db: Session = Depends(get_db)) -> BarberService:
    return BarberService(BarberRepository(db))


def error_response(exc: Exception) -> HTTPException:
    if isinstance(exc, BarberNotFoundError):
        return HTTPException(status_code=404, detail="Barbeiro não encontrado.")
    if isinstance(exc, UserAlreadyLinkedError):
        return HTTPException(status_code=409, detail="Este usuário já possui um perfil de barbeiro.")
    return HTTPException(status_code=422, detail="O usuário deve estar ativo e possuir perfil BARBER.")


@router.post("", response_model=BarberResponse, status_code=status.HTTP_201_CREATED)
def create_barber(
    data: BarberCreate,
    service: BarberService = Depends(get_service),
    _: User = Depends(admin_only),
) -> BarberResponse:
    try:
        return service.create(data)
    except (InvalidBarberUserError, UserAlreadyLinkedError) as exc:
        raise error_response(exc) from exc


@router.get("", response_model=list[BarberResponse])
def list_barbers(
    service: BarberService = Depends(get_service),
    _: User = Depends(staff_only),
) -> list[BarberResponse]:
    return service.list()


@router.get("/{barber_id}", response_model=BarberResponse)
def get_barber(
    barber_id: uuid.UUID,
    service: BarberService = Depends(get_service),
    _: User = Depends(staff_only),
) -> BarberResponse:
    try:
        return service.get(barber_id)
    except BarberNotFoundError as exc:
        raise error_response(exc) from exc


@router.patch("/{barber_id}", response_model=BarberResponse)
def update_barber(
    barber_id: uuid.UUID,
    data: BarberUpdate,
    service: BarberService = Depends(get_service),
    _: User = Depends(admin_only),
) -> BarberResponse:
    try:
        return service.update(barber_id, data)
    except BarberNotFoundError as exc:
        raise error_response(exc) from exc


@router.post(
    "/{barber_id}/unavailabilities",
    response_model=UnavailabilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_unavailability(
    barber_id: uuid.UUID,
    data: UnavailabilityCreate,
    service: BarberService = Depends(get_service),
    _: User = Depends(admin_only),
) -> UnavailabilityResponse:
    try:
        return service.add_unavailability(barber_id, data)
    except BarberNotFoundError as exc:
        raise error_response(exc) from exc


@router.get("/{barber_id}/unavailabilities", response_model=list[UnavailabilityResponse])
def list_unavailabilities(
    barber_id: uuid.UUID,
    service: BarberService = Depends(get_service),
    _: User = Depends(staff_only),
) -> list[UnavailabilityResponse]:
    try:
        return service.list_unavailabilities(barber_id)
    except BarberNotFoundError as exc:
        raise error_response(exc) from exc
