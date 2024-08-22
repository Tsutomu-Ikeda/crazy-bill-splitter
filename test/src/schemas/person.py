from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str = Field(..., min_length=1)
    paymentWeight : int = Field(1,gt=0)

    def __hash__(self) -> int:
        return hash(self.name)
