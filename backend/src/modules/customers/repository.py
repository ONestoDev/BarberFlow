import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.modules.customers.models import Customer


class DuplicatePhoneError(Exception):
    pass


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: uuid.UUID) -> Customer | None:
        statement = select(Customer).where(
            Customer.id == customer_id,
            Customer.active.is_(True),
        )
        return self.db.scalar(statement)

    def get_by_phone(self, phone: str) -> Customer | None:
        return self.db.scalar(select(Customer).where(Customer.phone == phone))

    def list_active(self, query: str | None, offset: int, limit: int) -> list[Customer]:
        statement = select(Customer).where(Customer.active.is_(True))
        if query:
            pattern = f"%{query.strip()}%"
            statement = statement.where(
                or_(
                    Customer.name.ilike(pattern),
                    Customer.phone.ilike(pattern),
                    Customer.email.ilike(pattern),
                )
            )
        statement = statement.order_by(Customer.name).offset(offset).limit(limit)
        return list(self.db.scalars(statement))

    def save(self, customer: Customer) -> Customer:
        self.db.add(customer)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise DuplicatePhoneError from exc
        self.db.refresh(customer)
        return customer

    def deactivate(self, customer: Customer) -> Customer:
        customer.active = False
        customer.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(customer)
        return customer
