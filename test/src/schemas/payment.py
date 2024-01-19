from decimal import Decimal
import enum

from pydantic import BaseModel, Field

from .person import Person


class Payment(BaseModel):
    amount: int = Field(..., gt=0)
    paid_by: Person = Field(...)
    paid_for: list[Person] = Field(..., min_length=1)


class Settlement(BaseModel):
    send_by: Person = Field(...)
    send_for: Person = Field(...)
    amount: Decimal = Field(..., decimal_places=2)

    def __str__(self) -> str:
        return f"{self.send_by.name} sends {self.amount} to {self.send_for.name}"

    def __repr__(self) -> str:
        return self.__str__()


class Constraint(enum.StrEnum):
    send_once = "send-once"
