from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any, Generic, TypeVar
from uuid import uuid4

from faker import Faker

T = TypeVar("T")


class BaseFactory(Generic[T]):
    """Base factory for generating deterministic test data."""

    _faker = Faker()
    _model: type[T]

    @classmethod
    def build(cls, **overrides: Any) -> T:
        payload = cls._default_payload()
        payload.update(overrides)
        return cls._model(**payload)

    @classmethod
    def build_many(cls, count: int, **overrides: Any) -> list[T]:
        return [cls.build(**overrides) for _ in range(count)]

    @classmethod
    def as_dict(cls, **overrides: Any) -> dict[str, Any]:
        return asdict(cls.build(**overrides))

    @classmethod
    def _default_payload(cls) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True)
class UserData:
    first_name: str
    last_name: str
    email: str
    password: str
    company: str = "QA Corp"


@dataclass(frozen=True)
class ProductData:
    name: str
    sku: str
    price: float
    category: str


class UserFactory(BaseFactory[UserData]):
    _model = UserData

    @classmethod
    def _default_payload(cls) -> dict[str, Any]:
        first_name = cls._faker.first_name()
        last_name = cls._faker.last_name()
        return {
            "first_name": first_name,
            "last_name": last_name,
            "email": f"qa_{uuid4().hex[:10]}@mailinator.com",
            "password": "TestPass123!",
            "company": cls._faker.company(),
        }


class ProductFactory(BaseFactory[ProductData]):
    _model = ProductData

    @classmethod
    def _default_payload(cls) -> dict[str, Any]:
        return {
            "name": cls._faker.catch_phrase(),
            "sku": cls._faker.bothify(text="SKU-####-??").upper(),
            "price": round(cls._faker.pyfloat(min_value=5, max_value=500, right_digits=2), 2),
            "category": cls._faker.word().title(),
        }


def dump_dataclass(instance: Any) -> dict[str, Any]:
    return {field.name: getattr(instance, field.name) for field in fields(instance)}
