from decimal import Decimal
from fractions import Fraction

import schemas


def calculate_settlements_send_once(*, payments: list[schemas.Payment], participants: list[schemas.Person]) -> list[schemas.Settlement]:
    receivable_amounts = {person: Fraction(0, 1) for person in participants}

    for payment in payments:
        receivable_amounts[payment.paid_by] += Fraction(payment.amount * len([person for person in payment.paid_for if person != payment.paid_by]), len(payment.paid_for))

        for person in payment.paid_for:
            if person == payment.paid_by:
                continue

            receivable_amounts[person] -= Fraction(payment.amount, len(payment.paid_for))

    settlements = []

    while True:
        person_with_min_receivable_amount = min(receivable_amounts, key=lambda person: receivable_amounts[person])
        exchange_amount = -receivable_amounts[person_with_min_receivable_amount]

        if receivable_amounts[person_with_min_receivable_amount] >= -1:
            break

        perfect_receive_candidates = sorted(
            (
                person
                for person in receivable_amounts
                if receivable_amounts[person] >= exchange_amount
            ),
            key=lambda person: receivable_amounts[person],
        )

        if len(perfect_receive_candidates) >= 1:
            receivable_amounts[person_with_min_receivable_amount] += exchange_amount
            receivable_amounts[perfect_receive_candidates[0]] -= exchange_amount
            settlements.append(
                schemas.Settlement(
                    send_by=person_with_min_receivable_amount,
                    send_for=perfect_receive_candidates[0],
                    amount=Decimal(f"{float(exchange_amount):.2f}"),
                )
            )
            continue

        imperfect_receive_candidates = sorted(
            (
                person
                for person in receivable_amounts
                if receivable_amounts[person] > 0
            ),
            key=lambda person: receivable_amounts[person],
            reverse=True,
        )

        if len(imperfect_receive_candidates) >= 1:
            receivable_amounts[person_with_min_receivable_amount] += exchange_amount
            receivable_amounts[imperfect_receive_candidates[0]] -= exchange_amount
            settlements.append(
                schemas.Settlement(
                    send_by=person_with_min_receivable_amount,
                    send_for=imperfect_receive_candidates[0],
                    amount=Decimal(f"{float(exchange_amount):.2f}"),
                )
            )
            continue

    return settlements
