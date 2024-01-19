import pytest

import schemas


def test_payment_participants():
    with pytest.raises(ValueError) as e:
        schemas.Settlement(
            send_by=schemas.Person(name="hoge"),
            amount="0.2"  # type: ignore
        )

    assert "1 validation error for Settlement\nsend_for\n  Field required" in str(e.value)

    with pytest.raises(ValueError) as e:
        schemas.Settlement(
            send_for=schemas.Person(name="hoge"),
            amount="0.2"  # type: ignore
        )

    assert "1 validation error for Settlement\nsend_by\n  Field required" in str(e.value)


def test_amount():
    settlement = schemas.Settlement(
        send_by=schemas.Person(name="hoge"),
        send_for=schemas.Person(name="fuga"),
        amount="0.2"  # type: ignore
    )
    assert settlement.amount * 5 == 1

    settlement2 = schemas.Settlement(
        send_by=schemas.Person(name="hoge"),
        send_for=schemas.Person(name="fuga"),
        amount="0.02"  # type: ignore
    )
    assert float(settlement2.amount) == 0.02

    with pytest.raises(ValueError) as e:
        schemas.Settlement(
            send_by=schemas.Person(name="hoge"),
            send_for=schemas.Person(name="fuga"),
            amount="0.021"  # type: ignore
        )

    assert "Decimal input should have no more than 2 decimal places" in str(e.value)
