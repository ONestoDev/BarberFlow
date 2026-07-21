import uuid

from src.modules.customers.models import Customer
from src.modules.customers.repository import CustomerRepository, DuplicatePhoneError
from src.modules.customers.schemas import CustomerCreate, CustomerUpdate


class CustomerNotFoundError(Exception):
    pass


class PhoneAlreadyInUseError(Exception):
    pass


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def create(self, data: CustomerCreate) -> Customer:
        if self.repository.get_by_phone(data.phone) is not None:
            raise PhoneAlreadyInUseError
        customer = Customer(
            name=data.name,
            phone=data.phone,
            email=str(data.email).lower() if data.email else None,
            notes=data.notes,
        )
        return self._save(customer)

    def get(self, customer_id: uuid.UUID) -> Customer:
        customer = self.repository.get_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError
        return customer

    def list(self, query: str | None, offset: int, limit: int) -> list[Customer]:
        return self.repository.list_active(query, offset, limit)

    def update(self, customer_id: uuid.UUID, data: CustomerUpdate) -> Customer:
        customer = self.get(customer_id)
        changes = data.model_dump(exclude_unset=True)
        new_phone = changes.get("phone")
        if new_phone and new_phone != customer.phone:
            existing = self.repository.get_by_phone(new_phone)
            if existing is not None:
                raise PhoneAlreadyInUseError
        if "email" in changes and changes["email"] is not None:
            changes["email"] = str(changes["email"]).lower()
        for field, value in changes.items():
            if field in {"name", "phone"} and value is None:
                continue
            setattr(customer, field, value)
        return self._save(customer)

    def deactivate(self, customer_id: uuid.UUID) -> Customer:
        return self.repository.deactivate(self.get(customer_id))

    def _save(self, customer: Customer) -> Customer:
        try:
            return self.repository.save(customer)
        except DuplicatePhoneError as exc:
            raise PhoneAlreadyInUseError from exc
