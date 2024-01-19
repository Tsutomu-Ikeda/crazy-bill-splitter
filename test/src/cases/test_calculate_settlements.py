from pydantic import BaseModel, Field
from decimal import Decimal
import pytest

import schemas
import services


class SettlementsConstraints(BaseModel):
    settlements_length: int = Field(...)
    receive_amount: dict[schemas.Person, Decimal] = Field(...)
    total_exchange_amount: Decimal = Field(...)


@pytest.mark.parametrize(
        "comment, request_body, expected_settlements_constraints",
        [
            (
                "fugaの5000円をhogeが建て替えたケース",
                services.CalculateSettlementRequestBody(
                    participants=[
                        schemas.Person(name="hoge"),
                        schemas.Person(name="fuga"),
                        schemas.Person(name="piyo"),
                    ],
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="hoge"),
                            paid_for=[schemas.Person(name="fuga")],
                            amount=5000,
                        ),
                    ]
                ),
                SettlementsConstraints(
                    settlements_length=1,
                    receive_amount={
                        schemas.Person(name="hoge"): Decimal(5000),
                        schemas.Person(name="fuga"): Decimal(-5000),
                        schemas.Person(name="piyo"): Decimal(0),
                    },
                    total_exchange_amount=Decimal(5000),
                )
            ),
            (
                "A,Bがそれぞれ全員分の5,000円を支払ったケース",
                services.CalculateSettlementRequestBody(
                    participants=[
                        schemas.Person(name="A"),
                        schemas.Person(name="B"),
                        schemas.Person(name="C"),
                        schemas.Person(name="D"),
                        schemas.Person(name="E"),
                    ],
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=[
                                schemas.Person(name="A"),
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                                schemas.Person(name="D"),
                                schemas.Person(name="E"),
                            ],
                            amount=5000,
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=[
                                schemas.Person(name="A"),
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                                schemas.Person(name="D"),
                                schemas.Person(name="E"),
                            ],
                            amount=5000,
                        ),
                    ]
                ),
                SettlementsConstraints(
                    settlements_length=4,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(3000),
                        schemas.Person(name="B"): Decimal(3000),
                        schemas.Person(name="C"): Decimal(-2000),
                        schemas.Person(name="D"): Decimal(-2000),
                        schemas.Person(name="E"): Decimal(-2000),
                    },
                    total_exchange_amount=Decimal(6000)
                )
            ),
            (
                "A,B,Cがそれぞれ全員分の5,000円を支払ったケース",
                services.CalculateSettlementRequestBody(
                    participants=[
                        schemas.Person(name="A"),
                        schemas.Person(name="B"),
                        schemas.Person(name="C"),
                        schemas.Person(name="D"),
                        schemas.Person(name="E"),
                    ],
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=[
                                schemas.Person(name="A"),
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                                schemas.Person(name="D"),
                                schemas.Person(name="E"),
                            ],
                            amount=5000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=[
                                schemas.Person(name="A"),
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                                schemas.Person(name="D"),
                                schemas.Person(name="E"),
                            ],
                            amount=5000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=[
                                schemas.Person(name="A"),
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                                schemas.Person(name="D"),
                                schemas.Person(name="E"),
                            ],
                            amount=5000
                        ),
                    ]
                ),
                SettlementsConstraints(
                    settlements_length=4,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(2000),
                        schemas.Person(name="B"): Decimal(2000),
                        schemas.Person(name="C"): Decimal(2000),
                        schemas.Person(name="D"): Decimal(-3000),
                        schemas.Person(name="E"): Decimal(-3000),
                    },
                    total_exchange_amount=Decimal(6000)
                )
            ),
            (
                "循環して5,000円ずつ支払ったケース",
                services.CalculateSettlementRequestBody(
                    participants=[
                        schemas.Person(name="A"),
                        schemas.Person(name="B"),
                        schemas.Person(name="C"),
                    ],
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=[
                                schemas.Person(name="B"),
                            ],
                            amount=5000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=[
                                schemas.Person(name="C"),
                            ],
                            amount=5000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=[
                                schemas.Person(name="A"),
                            ],
                            amount=5000
                        ),
                    ]
                ),
                SettlementsConstraints(
                    settlements_length=0,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(0),
                        schemas.Person(name="B"): Decimal(0),
                        schemas.Person(name="C"): Decimal(0),
                    },
                    total_exchange_amount=Decimal(0)
                )
            ),
            (
                "B,CがA,D,Eに精算を行う必要があるケース",
                services.CalculateSettlementRequestBody(
                    participants=[
                        schemas.Person(name="A"),
                        schemas.Person(name="B"),
                        schemas.Person(name="C"),
                        schemas.Person(name="D"),
                        schemas.Person(name="E"),
                    ],
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=[
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                            ],
                            amount=2500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=[
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                            ],
                            amount=2500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=[
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                            ],
                            amount=1000
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=4,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(1000),
                        schemas.Person(name="B"): Decimal(-3000),
                        schemas.Person(name="C"): Decimal(-3000),
                        schemas.Person(name="D"): Decimal(2500),
                        schemas.Person(name="E"): Decimal(2500),
                    },
                    total_exchange_amount=Decimal(6000)
                )
            ),
            (
                "3人で割り勘をして、割り切れないケース",
                services.CalculateSettlementRequestBody(
                    participants=[
                        schemas.Person(name="A"),
                        schemas.Person(name="B"),
                        schemas.Person(name="C"),
                    ],
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=[
                                schemas.Person(name="A"),
                                schemas.Person(name="B"),
                                schemas.Person(name="C"),
                            ],
                            amount=1000
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=2,
                    receive_amount={
                        schemas.Person(name="A"): Decimal("666.66"),
                        schemas.Person(name="B"): Decimal("-333.33"),
                        schemas.Person(name="C"): Decimal("-333.33"),
                    },
                    total_exchange_amount=Decimal("666.66")
                )
            )
        ]
)
def test_normal(comment: str, request_body: services.CalculateSettlementRequestBody, expected_settlements_constraints: SettlementsConstraints):
    actual_settlements = services.calculate_settlements(request_body)

    assert len(actual_settlements.settlements) <= expected_settlements_constraints.settlements_length, comment
    for person, expected_receive_amount in expected_settlements_constraints.receive_amount.items():
        sum_send_amount = sum(
            [
                settlement.amount
                for settlement in actual_settlements.settlements
                if settlement.send_by == person
            ]
        )
        sum_receive_amount = sum(
            [
                settlement.amount
                for settlement in actual_settlements.settlements
                if settlement.send_for == person
            ]
        )
        assert sum_receive_amount - sum_send_amount == expected_receive_amount, comment
    assert sum(
        [
            settlement.amount
            for settlement in actual_settlements.settlements
        ]
    ) == expected_settlements_constraints.total_exchange_amount, comment
