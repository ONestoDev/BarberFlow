import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.modules.auth.dependencies import require_roles
from src.modules.finance.repository import FinanceRepository
from src.modules.finance.schemas import CashFlowSummary, CorrectionCreate, TransactionCreate, TransactionResponse
from src.modules.finance.service import FinanceService, TransactionAlreadyCorrectedError, TransactionNotFoundError
from src.modules.users.models import User
from src.shared.database.connection import get_db
from src.shared.database.enums import FinancialTransactionType, UserRole

router = APIRouter(prefix="/finance", tags=["Financeiro"])
admin_only = require_roles(UserRole.ADMIN)


def get_service(db: Session = Depends(get_db)):
    return FinanceService(FinanceRepository(db))


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def create_transaction(data: TransactionCreate, service=Depends(get_service), user: User = Depends(admin_only)):
    return service.create(data, user.id)


@router.get("/transactions", response_model=list[TransactionResponse])
def list_transactions(
    starts_at: datetime,
    ends_at: datetime,
    transaction_type: FinancialTransactionType | None = None,
    service=Depends(get_service),
    _: User = Depends(admin_only),
):
    try: return service.list(starts_at, ends_at, transaction_type)
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc


@router.get("/summary", response_model=CashFlowSummary)
def get_summary(starts_at: datetime, ends_at: datetime, service=Depends(get_service), _: User = Depends(admin_only)):
    try: return service.summary(starts_at, ends_at)
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc


@router.post("/transactions/{transaction_id}/corrections", response_model=TransactionResponse, status_code=201)
def correct_transaction(
    transaction_id: uuid.UUID,
    data: CorrectionCreate,
    service=Depends(get_service),
    user: User = Depends(admin_only),
):
    try: return service.correct(transaction_id, data, user.id)
    except TransactionNotFoundError as exc: raise HTTPException(404, "Movimentação não encontrada.") from exc
    except TransactionAlreadyCorrectedError as exc: raise HTTPException(409, "Movimentação já corrigida ou é uma correção.") from exc
