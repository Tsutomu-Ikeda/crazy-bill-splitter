from pydantic import BaseModel, Field
from decimal import Decimal
import pytest

import schemas
import services
import helpers


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
                    participants=helpers.People.alphabetical_range("A", "E").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=5000,
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
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
                    participants=helpers.People.alphabetical_range("A", "E").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=5000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=5000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
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
                    participants=helpers.People.alphabetical_range("A", "C").members,
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
                    participants=helpers.People.alphabetical_range("A", "E").members,
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
                "連結でないグラフが発生しうるケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "E").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=13000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=12000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=11500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=6000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=2500
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=3,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(4000),
                        schemas.Person(name="B"): Decimal(3000),
                        schemas.Person(name="C"): Decimal(2500),
                        schemas.Person(name="D"): Decimal(-3000),
                        schemas.Person(name="E"): Decimal(-6500),
                    },
                    total_exchange_amount=Decimal(9500)
                )
            ),
            (
                "連結でないグラフが発生しうるケース 最大支払い者が最大受け取り者に支払うというロジックが使えないケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "E").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=9000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=8000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=3500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=2500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=helpers.People.alphabetical_range("A", "E").members,
                            amount=2000
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=3,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(4000),
                        schemas.Person(name="B"): Decimal(3000),
                        schemas.Person(name="C"): Decimal(-1500),
                        schemas.Person(name="D"): Decimal(-2500),
                        schemas.Person(name="E"): Decimal(-3000),
                    },
                    total_exchange_amount=Decimal(7000)
                )
            ),
            (
                "連結でないグラフが発生しうるケース 最大支払い者が最小可能受け取り者に支払うというロジックが使えないケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "G").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=8500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=9000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=1000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=1000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=1000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="F"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=500
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=5,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(5500),
                        schemas.Person(name="B"): Decimal(6000),
                        schemas.Person(name="C"): Decimal(-2000),
                        schemas.Person(name="D"): Decimal(-2000),
                        schemas.Person(name="E"): Decimal(-2000),
                        schemas.Person(name="F"): Decimal(-2500),
                        schemas.Person(name="G"): Decimal(-3000),
                    },
                    total_exchange_amount=Decimal(11500)
                )
            ),
            (
                "部分和で最適化できるケース、複数の部分和が存在するケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "G").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=1000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=7000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "G").members,
                            amount=6000
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=5,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(-1000),
                        schemas.Person(name="B"): Decimal(-2000),
                        schemas.Person(name="C"): Decimal(5000),
                        schemas.Person(name="D"): Decimal(4000),
                        schemas.Person(name="E"): Decimal(-2000),
                        schemas.Person(name="F"): Decimal(-2000),
                        schemas.Person(name="G"): Decimal(-2000),
                    },
                    total_exchange_amount=Decimal(9000)
                )
            ),
            (
                "3の精算グループができるケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "J").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=2000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=1000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=7500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=7500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=1750
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="F"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=11750
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="H"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=2950
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="I"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=8050
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="J"),
                            paid_for=helpers.People.alphabetical_range("A", "J").members,
                            amount=2500
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=7,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(-2500),
                        schemas.Person(name="B"): Decimal(-3500),
                        schemas.Person(name="C"): Decimal(3000),
                        schemas.Person(name="D"): Decimal(3000),
                        schemas.Person(name="E"): Decimal(-2750),
                        schemas.Person(name="F"): Decimal(7250),
                        schemas.Person(name="G"): Decimal(-4500),
                        schemas.Person(name="H"): Decimal(-1550),
                        schemas.Person(name="I"): Decimal(3550),
                        schemas.Person(name="J"): Decimal(-2000),
                    },
                    total_exchange_amount=Decimal(16800)
                )
            ),
            (
                "20名で割り勘をしたケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "T").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=206
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=206
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=206
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=606
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=407
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="F"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=407
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="G"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=407
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="H"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=3
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="I"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=201
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="J"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=201
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="K"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=201
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="L"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=621
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="M"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=408
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="N"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=408
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="O"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=408
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="Q"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=509
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="R"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=434
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="S"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=101
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="T"),
                            paid_for=helpers.People.alphabetical_range("A", "T").members,
                            amount=180
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=15,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(-100),
                        schemas.Person(name="B"): Decimal(-100),
                        schemas.Person(name="C"): Decimal(-100),
                        schemas.Person(name="D"): Decimal(300),
                        schemas.Person(name="E"): Decimal(101),
                        schemas.Person(name="F"): Decimal(101),
                        schemas.Person(name="G"): Decimal(101),
                        schemas.Person(name="H"): Decimal(-303),
                        schemas.Person(name="I"): Decimal(-105),
                        schemas.Person(name="J"): Decimal(-105),
                        schemas.Person(name="K"): Decimal(-105),
                        schemas.Person(name="L"): Decimal(315),
                        schemas.Person(name="M"): Decimal(102),
                        schemas.Person(name="N"): Decimal(102),
                        schemas.Person(name="O"): Decimal(102),
                        schemas.Person(name="P"): Decimal(-306),
                        schemas.Person(name="Q"): Decimal(203),
                        schemas.Person(name="R"): Decimal(128),
                        schemas.Person(name="S"): Decimal(-205),
                        schemas.Person(name="T"): Decimal(-126),
                    },
                    total_exchange_amount=Decimal(1555)
                )
            ),
            (
                "単一リーダーのグループに貪欲的に分割しても最適解にたどり着けないケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "L").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=664
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=257
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=256
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=255
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=408
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="F"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=409
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="G"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=407
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="H"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=411
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="I"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=406
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="J"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=413
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="K"),
                            paid_for=helpers.People.alphabetical_range("A", "L").members,
                            amount=410
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=8,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(306),
                        schemas.Person(name="B"): Decimal(-101),
                        schemas.Person(name="C"): Decimal(-102),
                        schemas.Person(name="D"): Decimal(-103),
                        schemas.Person(name="E"): Decimal(50),
                        schemas.Person(name="F"): Decimal(51),
                        schemas.Person(name="G"): Decimal(49),
                        schemas.Person(name="H"): Decimal(53),
                        schemas.Person(name="I"): Decimal(48),
                        schemas.Person(name="J"): Decimal(55),
                        schemas.Person(name="K"): Decimal(52),
                        schemas.Person(name="L"): Decimal(-358),
                    },
                    total_exchange_amount=Decimal(664)
                )
            ),
            (
                "16名で1対1の送金で精算できるケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "P").members,
                    payments=[
                        schemas.Payment(
                            paid_by=paid_by,
                            paid_for=helpers.People.alphabetical_range("A", "P").members,
                            amount=600
                        )
                        for paid_by in helpers.People.alphabetical_range("A", "H").members
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=8,
                    receive_amount={
                        creditor: Decimal(300)
                        for creditor in helpers.People.alphabetical_range("A", "H").members
                    } | {
                        debtor: Decimal(-300)
                        for debtor in helpers.People.alphabetical_range("I", "P").members
                    },
                    total_exchange_amount=Decimal(2400)
                )
            ),
            (
                "min(m, n)が2のグループが2つできるケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "I").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=6000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="B"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=7000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="D"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=3500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="E"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=3500
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="F"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=9100
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="G"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=6200
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="H"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=300
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="I"),
                            paid_for=helpers.People.alphabetical_range("A", "I").members,
                            amount=400
                        ),
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=7,
                    receive_amount={
                        schemas.Person(name="A"): Decimal(2000),
                        schemas.Person(name="B"): Decimal(3000),
                        schemas.Person(name="C"): Decimal(-4000),
                        schemas.Person(name="D"): Decimal(-500),
                        schemas.Person(name="E"): Decimal(-500),
                        schemas.Person(name="F"): Decimal(5100),
                        schemas.Person(name="G"): Decimal(2200),
                        schemas.Person(name="H"): Decimal(-3700),
                        schemas.Person(name="I"): Decimal(-3600),
                    },
                    total_exchange_amount=Decimal(12300)
                )
            ),
            (
                "3人で割り勘をして、割り切れないケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.alphabetical_range("A", "C").members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A"),
                            paid_for=helpers.People.alphabetical_range("A", "C").members,
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
            ),
            (
                "傾斜ありで綺麗に分割できるケース",
                services.CalculateSettlementRequestBody(
                    participants=helpers.People.generate(3,weights=[3,2,2]).members,
                    payments=[
                        schemas.Payment(
                            paid_by=schemas.Person(name="A",paymentWeight=3),
                            paid_for=helpers.People.generate(3,weights=[3,2,2]).members,
                            amount=7000
                        ),
                        schemas.Payment(
                            paid_by=schemas.Person(name="C",paymentWeight=2),
                            paid_for=helpers.People.generate(3,weights=[3,2,2]).members,
                            amount=7000
                        )
                    ],
                ),
                SettlementsConstraints(
                    settlements_length=2,
                    receive_amount={
                        schemas.Person(name="A",paymentWeight=3): Decimal("1000"),
                        schemas.Person(name="B",paymentWeight=2): Decimal("-4000"),
                        schemas.Person(name="C",paymentWeight=2): Decimal("3000"),
                    },
                    total_exchange_amount=Decimal("4000")
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
    ) <= expected_settlements_constraints.total_exchange_amount, comment
