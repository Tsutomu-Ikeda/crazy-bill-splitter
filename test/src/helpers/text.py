import re
from pydantic import BaseModel

class Text(BaseModel):

    @staticmethod
    def alphabetical_range(begin: str, end: str) -> list[str]:
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

        return [chr(i) for i in range(ord(begin), ord(end) + 1)]
