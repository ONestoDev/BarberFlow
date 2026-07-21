import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from src.modules.auth.dependencies import require_roles
from src.modules.customers.repository import CustomerRepository
from src.modules.customers.schemas import CustomerCreate, CustomerResponse, CustomerUpdate
from src.modules.customers.service import (
    CustomerNotFoundError,
    CustomerService,
    PhoneAlreadyInUseError,
)
from src.modules.users.models import User
from src.shared.database.connection import get_db
from src.shared.database.enums import UserRole

router = APIRouter(prefix="/customers", tags=["Clientes"])
staff_only = require_roles(UserRole.ADMIN, UserRole.BARBER)


def get_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(CustomerRepository(db))


def translate_error(exc: Exception) -> HTTPException:
    if isinstance(exc, CustomerNotFoundError):
        return HTTPException(status_code=404, detail="Cliente não encontrado.")
    return HTTPException(status_code=409, detail="Já existe um cliente com este telefone.")


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    data: CustomerCreate,
    service: CustomerService = Depends(get_service),
    _: User = Depends(staff_only),
) -> CustomerResponse:
    try:
        return service.create(data)
    except PhoneAlreadyInUseError as exc:
        raise translate_error(exc) from exc


@router.get("", response_model=list[CustomerResponse])
def list_customers(
    q: str | None = Query(default=None, max_length=160),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    service: CustomerService = Depends(get_service),
    _: User = Depends(staff_only),
) -> list[CustomerResponse]:
    return service.list(q, offset, limit)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: uuid.UUID,
    service: CustomerService = Depends(get_service),
    _: User = Depends(staff_only),
) -> CustomerResponse:
    try:
        return service.get(customer_id)
    except CustomerNotFoundError as exc:
        raise translate_error(exc) from exc


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: uuid.UUID,
    data: CustomerUpdate,
    service: CustomerService = Depends(get_service),
    _: User = Depends(staff_only),
) -> CustomerResponse:
    try:
        return service.update(customer_id, data)
    except (CustomerNotFoundError, PhoneAlreadyInUseError) as exc:
        raise translate_error(exc) from exc


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_customer(
    customer_id: uuid.UUID,
    service: CustomerService = Depends(get_service),
    _: User = Depends(staff_only),
) -> Response:
    try:
        service.deactivate(customer_id)
    except CustomerNotFoundError as exc:
        raise translate_error(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
