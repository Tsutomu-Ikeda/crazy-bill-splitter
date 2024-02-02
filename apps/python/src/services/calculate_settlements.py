from decimal import Decimal
from fractions import Fraction

import schemas


def calculate_settlements(*, payments: list[schemas.Payment], participants: list[schemas.Person]) -> list[schemas.Settlement]:
    receivable_amounts = {person: Fraction(0, 1) for person in participants}

    for payment in payments:
        receivable_amounts[payment.paid_by] += Fraction(payment.amount * len([person for person in payment.paid_for if person != payment.paid_by]), len(payment.paid_for))

        for person in payment.paid_for:
            if person == payment.paid_by:
                continue

            receivable_amounts[person] -= Fraction(payment.amount, len(payment.paid_for))

    settlements = []

    positive_receivable_amounts = {
        person: receivable_amounts[person]
        for person in receivable_amounts
        if receivable_amounts[person] > 0
    }
    negative_receivable_amounts = {
        person: receivable_amounts[person]
        for person in receivable_amounts
        if receivable_amounts[person] < 0
    }

    if len(positive_receivable_amounts) <= len(negative_receivable_amounts):
        # negative_receivable_amountsの部分和でpositive_receivable_amountsの各要素を満たせるかどうかを調べる
        # できる場合、settlementsに追加する
        for person in positive_receivable_amounts:
            exchange_amount = positive_receivable_amounts[person]

            len_positive_receivable_amounts = len(negative_receivable_amounts)

            for bit in range(1 << len_positive_receivable_amounts):
                target_person = [
                    person
                    for i, person
                    in enumerate(negative_receivable_amounts)
                    if ((bit >> i) & 1) == 1
                ]

                if sum(-negative_receivable_amounts[person] for person in target_person) == exchange_amount:
                    for target in target_person:
                        settlements.append(
                            schemas.Settlement(
                                send_by=target,
                                send_for=person,
                                amount=Decimal(f"{float(-negative_receivable_amounts[target]):.2f}"),
                            )
                        )
                        receivable_amounts[target] = Fraction(0)
                        negative_receivable_amounts[target] = Fraction(0)

                    receivable_amounts[person] = Fraction(0)
    else:
        # positive_receivable_amountsの部分和でnegative_receivable_amountsの各要素を満たせるかどうかを調べる
        # できる場合、settlementsに追加する
        for person in negative_receivable_amounts:
            exchange_amount = -negative_receivable_amounts[person]

            len_negative_receivable_amounts = len(positive_receivable_amounts)

            for bit in range(1 << len_negative_receivable_amounts):
                target_person = [
                    person
                    for i, person
                    in enumerate(positive_receivable_amounts)
                    if ((bit >> i) & 1) == 1
                ]

                if sum(positive_receivable_amounts[person] for person in target_person) == exchange_amount:
                    for target in target_person:
                        settlements.append(
                            schemas.Settlement(
                                send_by=person,
                                send_for=target,
                                amount=Decimal(f"{float(positive_receivable_amounts[target]):.2f}"),
                            )
                        )
                        receivable_amounts[target] = Fraction(0)
                        positive_receivable_amounts[target] = Fraction(0)

                    receivable_amounts[person] = Fraction(0)

    while True:
        person_with_max_receivable_amount = max(receivable_amounts, key=lambda person: receivable_amounts[person])
        person_with_min_receivable_amount = min(receivable_amounts, key=lambda person: receivable_amounts[person])

        if receivable_amounts[person_with_max_receivable_amount] <= 1:
            break

        amount = min(
            receivable_amounts[person_with_max_receivable_amount],
            -receivable_amounts[person_with_min_receivable_amount],
        )

        settlements.append(
            schemas.Settlement(
                send_by=person_with_min_receivable_amount,
                send_for=person_with_max_receivable_amount,
                amount=Decimal(f"{float(amount):.2f}"),
            )
        )

        receivable_amounts[person_with_max_receivable_amount] -= amount
        receivable_amounts[person_with_min_receivable_amount] += amount

    return settlements
