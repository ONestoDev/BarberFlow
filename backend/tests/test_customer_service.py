import uuid
from datetime import datetime, timezone

import pytest

from src.modules.customers.models import Customer
from src.modules.customers.repository import DuplicatePhoneError
from src.modules.customers.schemas import CustomerCreate, CustomerUpdate
from src.modules.customers.service import (
    CustomerNotFoundError,
    CustomerService,
    PhoneAlreadyInUseError,
)


class FakeCustomerRepository:
    def __init__(self, customer=None, phone_match=None, duplicate_on_save=False):
        self.customer = customer
        self.phone_match = phone_match
        self.duplicate_on_save = duplicate_on_save

    def get_by_id(self, customer_id):
        return self.customer

    def get_by_phone(self, phone):
        return self.phone_match

    def list_active(self, query, offset, limit):
        return [self.customer] if self.customer else []

    def save(self, customer):
        if self.duplicate_on_save:
            raise DuplicatePhoneError
        self.customer = customer
        return customer

    def deactivate(self, customer):
        customer.active = False
        customer.deleted_at = datetime.now(timezone.utc)
        return customer


def make_customer() -> Customer:
    return Customer(
        id=uuid.uuid4(),
        user_id=None,
        name="Cliente Teste",
        phone="11999998888",
        email="cliente@example.com",
        notes=None,
        active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )


def customer_data() -> CustomerCreate:
    return CustomerCreate(
        name=" Cliente Novo ",
        phone="(11) 98888-7777",
        email="CLIENTE@example.com",
        notes="Prefere tesoura.",
    )


def test_create_customer_normalizes_fields():
    customer = CustomerService(FakeCustomerRepository()).create(customer_data())

    assert customer.name == "Cliente Novo"
    assert customer.phone == "11988887777"
    assert customer.email == "cliente@example.com"


def test_create_customer_rejects_duplicate_phone():
    repository = FakeCustomerRepository(phone_match=make_customer())

    with pytest.raises(PhoneAlreadyInUseError):
        CustomerService(repository).create(customer_data())


def test_create_customer_handles_unique_constraint_race():
    with pytest.raises(PhoneAlreadyInUseError):
        CustomerService(FakeCustomerRepository(duplicate_on_save=True)).create(customer_data())


def test_get_customer_rejects_unknown_id():
    with pytest.raises(CustomerNotFoundError):
        CustomerService(FakeCustomerRepository()).get(uuid.uuid4())


def test_update_customer_changes_allowed_fields():
    customer = make_customer()
    service = CustomerService(FakeCustomerRepository(customer=customer))

    updated = service.update(
        customer.id,
        CustomerUpdate(name="Nome Atualizado", email=None, notes="Nova observação"),
    )

    assert updated.name == "Nome Atualizado"
    assert updated.email is None
    assert updated.notes == "Nova observação"


def test_update_customer_rejects_phone_used_by_another_customer():
    customer = make_customer()
    repository = FakeCustomerRepository(customer=customer, phone_match=object())

    with pytest.raises(PhoneAlreadyInUseError):
        CustomerService(repository).update(
            customer.id, CustomerUpdate(phone="11911112222")
        )


def test_deactivate_customer_uses_soft_delete():
    customer = make_customer()

    result = CustomerService(FakeCustomerRepository(customer=customer)).deactivate(customer.id)

    assert result.active is False
    assert result.deleted_at is not None
