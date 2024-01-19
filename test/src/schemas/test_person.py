import pytest

import schemas


def test_person():
    person = schemas.Person(name="hoge")

    assert person.name == "hoge"

    with pytest.raises(ValueError) as e:
        schemas.Person(name="")

    assert "1 validation error for Person\nname\n  String should have at least 1 character" in str(e.value)

