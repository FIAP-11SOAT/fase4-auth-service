import uuid
from enum import Enum

from pydantic import BaseModel


class UserType(str, Enum):
    CUSTOMERS = "customers"
    EMPLOYEES = "employees"


class User(BaseModel):
    id: str
    tax_id: str
    email: str
    name: str
    user_type: UserType

    @classmethod
    def create_costumer(cls, tax_id: str, email: str, name: str) -> "User":
        return cls(
            id=str(uuid.uuid4()),
            tax_id=tax_id,
            email=email,
            name=name,
            user_type=UserType.CUSTOMERS,
        )
