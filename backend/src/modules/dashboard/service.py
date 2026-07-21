from datetime import timezone
from decimal import Decimal

from src.modules.dashboard.repository import DashboardRepository
from src.modules.dashboard.schemas import DashboardSummary, TopBarber, TopService


class DashboardService:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    def summary(self, starts_at, ends_at) -> DashboardSummary:
        if (
            starts_at.tzinfo is None
            or ends_at.tzinfo is None
            or starts_at >= ends_at
        ):
            raise ValueError("Período do dashboard inválido.")
        starts_at = starts_at.astimezone(timezone.utc)
        ends_at = ends_at.astimezone(timezone.utc)
        service_rows = self.repository.top_services(starts_at, ends_at)
        barber_row = self.repository.top_barber(starts_at, ends_at)
        return DashboardSummary(
            starts_at=starts_at,
            ends_at=ends_at,
            revenue=self.repository.revenue(starts_at, ends_at),
            completed_appointments=self.repository.completed_appointments(
                starts_at, ends_at
            ),
            new_customers=self.repository.new_customers(starts_at, ends_at),
            top_services=[
                TopService(service_id=row[0], name=row[1], quantity=row[2])
                for row in service_rows
            ],
            top_barber=(
                TopBarber(
                    barber_id=barber_row[0],
                    name=barber_row[1],
                    revenue=Decimal(str(barber_row[2])),
                )
                if barber_row
                else None
            ),
        )
