import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.barbers.models import Barber, BarberUnavailability
from src.modules.users.models import User


class BarberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: uuid.UUID) -> User | None:
        return self.db.get(User, user_id)

    def get_by_user_id(self, user_id: uuid.UUID) -> Barber | None:
        return self.db.scalar(select(Barber).where(Barber.user_id == user_id))

    def get_by_id(self, barber_id: uuid.UUID) -> Barber | None:
        return self.db.scalar(select(Barber).where(Barber.id == barber_id, Barber.active.is_(True)))

    def list_active(self) -> list[Barber]:
        return list(self.db.scalars(select(Barber).where(Barber.active.is_(True)).order_by(Barber.created_at)))

    def save(self, barber: Barber) -> Barber:
        self.db.add(barber)
        self.db.commit()
        self.db.refresh(barber)
        return barber

    def add_unavailability(self, item: BarberUnavailability) -> BarberUnavailability:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_unavailabilities(self, barber_id: uuid.UUID) -> list[BarberUnavailability]:
        statement = select(BarberUnavailability).where(
            BarberUnavailability.barber_id == barber_id
        ).order_by(BarberUnavailability.starts_at)
        return list(self.db.scalars(statement))
