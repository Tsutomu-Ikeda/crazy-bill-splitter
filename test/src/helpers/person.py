import re
from typing import Iterable, Optional

from pydantic import BaseModel
import schemas


class People(BaseModel):
    members: list[schemas.Person]

    @classmethod
    def alphabetical_range(cls, begin: str, end: str) -> "People":
        """
        Create a People object from a range of alphabetical characters.

        Args:
            begin (str): The first alphabetical character.
            end (str): The last alphabetical character.

        Returns:
            People: A People object with members from the range of alphabetical characters.

        Example:
            >>> People.alphabetical_range("A", "C")
            People(members=[Person(name='A'), Person(name='B'), Person(name='C')])
        """

        VALID_INPUT_REGEX = r"^[A-Z]$"

        errors = []

        if not re.match(VALID_INPUT_REGEX, begin):
            errors.append("begin must be a single uppercase alphabetical character")

        if not re.match(VALID_INPUT_REGEX, end):
            errors.append("end must be a single uppercase alphabetical character")

        if begin > end:
            errors.append("begin must be less than or equal to end")

        if errors:
            raise ValueError(f"{len(errors)} errors occurred:\n\n" + "\n".join(errors))

        return cls(members=[schemas.Person(name=chr(i)) for i in range(ord(begin), ord(end) + 1)])

    @classmethod
    def generate(cls, count: int, names: Optional[Iterable[int]] = None, weights: Optional[Iterable[int]] = None) -> "People":
        """
        Create a People object with a specified number of members.

        Args:
            count (int): The number of members to generate.

        Returns:
            People: A People object with the specified number of members.

        Example:
            >>> People.generate(3)
            People(members=[Person(name='A'), Person(name='B'), Person(name='C')])
        """

        if count < 0:
            raise ValueError("count must be greater than or equal to 0")
        if names != None and len(names) != count:
            raise ValueError("count must be equal to the length of names")
        if weights != None and len(weights) != count:
            raise ValueError("count must be equal to the length of weights")

        if names != None and weights != None:
            return cls(members=[schemas.Person(name=name,paymentWeight=weight) for name, weight in zip(names, weights) ])
        elif names != None:
            return cls(members=[schemas.Person(name=name) for name in names])
        elif weights != None:
            return cls(members=[schemas.Person(name=chr(i + ord('A')),paymentWeight=weights[i]) for i in range(count)])
        else:
            return cls(members=[schemas.Person(name=chr(i + ord('A')) ) for i in range(count)])
