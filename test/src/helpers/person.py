import re
from typing import Optional

from pydantic import BaseModel
import schemas


class People(BaseModel):
    members: list[schemas.Person]

    @classmethod
    def alphabetical_range(cls, begin: str, end: str,weights: Optional[list[int]] = None) -> "People":
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

        if weights == None:
            return cls(members=[schemas.Person(name=chr(i)) for i in range(ord(begin), ord(end) + 1)])
        else:
            if any(weights < 0 for weights in weights):
                raise ValueError("weights must be greater than or equal to 0")
            if len(weights) != ord(end) - ord(begin) + 1:
                raise ValueError("weights must have the same length as the range of characters")
            return cls(members=[schemas.Person(name=chr(i),paymentWeight=weights[i-ord(begin)]) for i in range(ord(begin), ord(end) + 1)])
