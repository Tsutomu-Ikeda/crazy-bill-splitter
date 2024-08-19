from typing import Iterable, Optional

from pydantic import BaseModel
import schemas


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

        if names == None and paymentWeights == None:
            raise ValueError("names and weights cannot both be None")

        if names != None and paymentWeights != None:
            return cls(members=[schemas.Person(name=name,paymentWeight=weights) for name, weights in zip(names, paymentWeights) ])
        elif names != None:
            return cls(members=[schemas.Person(name=name) for name in names])
        elif paymentWeights != None:
            return cls(members=[schemas.Person(name=chr(i + ord('A')),paymentWeight=paymentWeights[i]) for i in range(len(paymentWeights))])
