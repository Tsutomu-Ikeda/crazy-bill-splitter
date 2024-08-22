from typing import Iterable, Optional
from pydantic import BaseModel
import schemas
from .text import Text
from itertools import repeat


class People(BaseModel):
    members: list[schemas.Person]

    @classmethod
    def generate(cls,names: Optional[Iterable[str]] = None, paymentWeights: Optional[Iterable[int]] = None) -> "People":
        """
        Create a People object with a specified number of members.

        Args:
            names (Optional[Iterable[int]]): A list of names for the members.
            weights (Optional[Iterable[int]]): A list of weights for the members.
        Returns:
            People: A People object with the specified number of members.

        Example:
            >>> People.generate(names=["Alice", "Bob", "Charlie"], weights=[1, 2, 3])
            People(members=[Person(name='Alice', paymentWeight=1), Person(name='Bob', paymentWeight=2), Person(name='Charlie', paymentWeight=3)])
        """
        def determine_members_count() -> int:  
            if names != None:  
                return len(names)  
            elif paymentWeights != None:  
                return len(paymentWeights)  

            raise ValueError("names and weights cannot both be None")  

        members_count = determine_members_count()

        return cls(
        members=[
            schemas.Person(
            name=name,
            paymentWeight=paymentWeight
            )
            for name, paymentWeight
            in zip(
            names or Text.alphabetical_range("A", chr(members_count - 1 + ord('A'))),
            paymentWeights or repeat(1)
            )
        ]
        )

