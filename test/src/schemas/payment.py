from pydantic import BaseModel, Field
from decimal import Decimal

from .person import Person


class Payment(BaseModel):
    amount: int = Field(..., gt=0)
    paid_by: Person = Field(...)
    paid_for: list[Person] = Field(..., min_length=1)


class Settlement(BaseModel):
    send_by: Person = Field(...)
    send_for: Person = Field(...)
    amount: Decimal = Field(..., gt=0, le=100_000, decimal_places=2)
