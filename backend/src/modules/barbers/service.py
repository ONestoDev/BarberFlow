import uuid

from src.modules.barbers.models import Barber, BarberSchedule, BarberSpecialty, BarberUnavailability
from src.modules.barbers.repository import BarberRepository
from src.modules.barbers.schemas import BarberCreate, BarberUpdate, ScheduleInput, UnavailabilityCreate
from src.shared.database.enums import UserRole


class BarberNotFoundError(Exception):
    pass


class InvalidBarberUserError(Exception):
    pass


class UserAlreadyLinkedError(Exception):
    pass


class BarberService:
    def __init__(self, repository: BarberRepository):
        self.repository = repository

    def create(self, data: BarberCreate) -> Barber:
        user = self.repository.get_user(data.user_id)
        if user is None or not user.active or user.role != UserRole.BARBER:
            raise InvalidBarberUserError
        if self.repository.get_by_user_id(data.user_id) is not None:
            raise UserAlreadyLinkedError
        barber = Barber(user_id=data.user_id, bio=data.bio)
        self._replace_details(barber, data.specialties, data.schedules)
        return self.repository.save(barber)

    def get(self, barber_id: uuid.UUID) -> Barber:
        barber = self.repository.get_by_id(barber_id)
        if barber is None:
            raise BarberNotFoundError
        return barber

    def list(self) -> list[Barber]:
        return self.repository.list_active()

    def update(self, barber_id: uuid.UUID, data: BarberUpdate) -> Barber:
        barber = self.get(barber_id)
        if "bio" in data.model_fields_set:
            barber.bio = data.bio
        specialties = data.specialties if "specialties" in data.model_fields_set else None
        schedules = data.schedules if "schedules" in data.model_fields_set else None
        self._replace_details(barber, specialties, schedules)
        return self.repository.save(barber)

    def add_unavailability(self, barber_id: uuid.UUID, data: UnavailabilityCreate) -> BarberUnavailability:
        self.get(barber_id)
        return self.repository.add_unavailability(
            BarberUnavailability(barber_id=barber_id, **data.model_dump())
        )

    def list_unavailabilities(self, barber_id: uuid.UUID) -> list[BarberUnavailability]:
        self.get(barber_id)
        return self.repository.list_unavailabilities(barber_id)

    @staticmethod
    def _replace_details(
        barber: Barber,
        specialties: list[str] | None,
        schedules: list[ScheduleInput] | None,
    ) -> None:
        if specialties is not None:
            barber.specialties = [BarberSpecialty(name=name) for name in specialties]
        if schedules is not None:
            barber.schedules = [BarberSchedule(**item.model_dump()) for item in schedules]
