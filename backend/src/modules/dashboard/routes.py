from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.modules.auth.dependencies import require_roles
from src.modules.dashboard.repository import DashboardRepository
from src.modules.dashboard.schemas import DashboardSummary
from src.modules.dashboard.service import DashboardService
from src.modules.users.models import User
from src.shared.database.connection import get_db
from src.shared.database.enums import UserRole

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
admin_only = require_roles(UserRole.ADMIN)


def get_service(db: Session = Depends(get_db)):
    return DashboardService(DashboardRepository(db))


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    starts_at: datetime,
    ends_at: datetime,
    service=Depends(get_service),
    _: User = Depends(admin_only),
):
    try:
        return service.summary(starts_at, ends_at)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
