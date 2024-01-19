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

    for person in receivable_amounts:
        if receivable_amounts[person] >= 0:
            continue

        perfect_receive_candidates = sorted(
            (
                receive_person
                for receive_person in receivable_amounts
                if receivable_amounts[receive_person] == -receivable_amounts[person]
            ),
            key=lambda p: receivable_amounts[p],
        )

        if len(perfect_receive_candidates) >= 1:
            exchange_amount = -receivable_amounts[person]
            receivable_amounts[person] += exchange_amount
            receivable_amounts[perfect_receive_candidates[0]] -= exchange_amount
            settlements.append(
                schemas.Settlement(
                    send_by=person,
                    send_for=perfect_receive_candidates[0],
                    amount=Decimal(f"{float(exchange_amount):.2f}"),
                )
            )

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
