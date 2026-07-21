import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.modules.auth.dependencies import require_roles
from src.modules.payments.repository import PaymentRepository
from src.modules.payments.schemas import PaymentCreate, PaymentResponse
from src.modules.payments.service import (
    AppointmentAlreadyPaidError,
    InvalidDiscountError,
    PayableAppointmentNotFoundError,
    PaymentService,
    ZeroValuePaymentError,
)
from src.modules.users.models import User
from src.shared.database.connection import get_db
from src.shared.database.enums import UserRole

router = APIRouter(prefix="/appointments/{appointment_id}/payment", tags=["Pagamentos"])
staff_only = require_roles(UserRole.ADMIN, UserRole.BARBER)


def get_service(db: Session = Depends(get_db)):
    return PaymentService(PaymentRepository(db))


def translate_error(exc):
    if isinstance(exc, PayableAppointmentNotFoundError):
        return HTTPException(404, "Atendimento não encontrado, cancelado ou sem pagamento.")
    if isinstance(exc, AppointmentAlreadyPaidError):
        return HTTPException(409, "Este atendimento já possui pagamento registrado.")
    if isinstance(exc, InvalidDiscountError):
        return HTTPException(422, "O desconto não pode superar o valor original.")
    return HTTPException(422, "O valor final do pagamento deve ser maior que zero.")


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    appointment_id: uuid.UUID,
    data: PaymentCreate,
    service=Depends(get_service),
    user: User = Depends(staff_only),
):
    try:
        return service.create(appointment_id, data, user.id)
    except (
        PayableAppointmentNotFoundError,
        AppointmentAlreadyPaidError,
        InvalidDiscountError,
        ZeroValuePaymentError,
    ) as exc:
        raise translate_error(exc) from exc


@router.get("", response_model=PaymentResponse)
def get_payment(
    appointment_id: uuid.UUID,
    service=Depends(get_service),
    _: User = Depends(staff_only),
):
    try:
        return service.get_by_appointment(appointment_id)
    except PayableAppointmentNotFoundError as exc:
        raise translate_error(exc) from exc
