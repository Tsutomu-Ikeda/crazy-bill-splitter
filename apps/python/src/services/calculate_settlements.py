from decimal import Decimal
from fractions import Fraction
import itertools

import schemas


def calculate_settlements(*, payments: list[schemas.Payment], participants: list[schemas.Person]) -> list[schemas.Settlement]:
    receivable_amounts = __calculate_receivable_amounts(payments=payments, participants=participants)
    settlement_groups = __create_settlement_groups_recursively(receivable_amounts=receivable_amounts)

    settlements = list(itertools.chain.from_iterable(
        __create_settlements_greedy(
            receivable_amounts={person: receivable_amounts[person] for person in settlement_group},
        )
        for settlement_group in settlement_groups
    ))

    return settlements


def __calculate_receivable_amounts(*, payments: list[schemas.Payment], participants: list[schemas.Person]) -> dict[schemas.Person, Fraction]:
    receivable_amounts = {person: Fraction(0, 1) for person in participants}

    for payment in payments:
        total_weight = sum([participant.paymentWeight for participant in payment.paid_for])
        receivable_amounts[payment.paid_by] += Fraction(payment.amount * sum([person.paymentWeight for person in payment.paid_for if person != payment.paid_by]), total_weight)

        for person in payment.paid_for:
            if person == payment.paid_by:
                continue

            receivable_amounts[person] -= Fraction(payment.amount * person.paymentWeight, total_weight)

    return receivable_amounts


__create_settlement_groups_recursively_memo = dict()


def __create_settlement_groups_recursively(*, receivable_amounts: dict[schemas.Person, Fraction]) -> list[list[schemas.Person]]:
    memo_key = "-".join(sorted(f"{person.name},{receivable_amounts[person]}" for person in receivable_amounts))

    if memo_key in __create_settlement_groups_recursively_memo:
        return __create_settlement_groups_recursively_memo[memo_key]

    if len(receivable_amounts) == 0:
        return []

    # 債務者
    debtors = {person: receivable_amounts[person] for person in receivable_amounts if receivable_amounts[person] < 0}
    # 債権者
    creditors = {person: receivable_amounts[person] for person in receivable_amounts if receivable_amounts[person] > 0}

    # 債務者の数nが1の場合、精算グループはこれ以上分割できないので、そのまま返す
    if len(debtors) == 1:
        return [[person for person in receivable_amounts]]

    # 債権者の数nが1の場合、精算グループはこれ以上分割できないので、そのまま返す
    if len(creditors) == 1:
        return [[person for person in receivable_amounts]]

    queue = []
    visited = set()

    for i in range(1, 1 << len(debtors)):
        sub_debtors = {
            person
            for k, person
            in enumerate(debtors)
            if ((i >> k) & 1) == 1
        }

        # NOTE: 名前ではなく金額のみで判断することで、組み合わせを減らす
        sub_debtors_text = ";".join(sorted(str(receivable_amounts[p]) for p in sub_debtors))

        for j in range(1, 1 << len(creditors)):
            sub_creditors = {
                person
                for k, person
                in enumerate(creditors)
                if ((j >> k) & 1) == 1
            }
            sub_creditors_text = ";".join(sorted(str(receivable_amounts[p]) for p in sub_creditors))

            if f"{sub_debtors_text}:{sub_creditors_text}" in visited:
                continue

            visited.add(f"{sub_debtors_text}:{sub_creditors_text}")

            if sum(-receivable_amounts[person] for person in sub_debtors) == sum(receivable_amounts[person] for person in sub_creditors):
                if len(sub_debtors) + len(sub_creditors) == 0 or len(sub_debtors) + len(sub_creditors) == len(receivable_amounts):
                    continue

                sub_group_left = {person: receivable_amounts[person] for person in receivable_amounts if person not in (sub_debtors | sub_creditors)}
                sub_group_right = {person: receivable_amounts[person] for person in receivable_amounts if person in (sub_debtors | sub_creditors)}
                queue.append((sub_group_left, sub_group_right))

    candidates = []

    for sub_group_left, sub_group_right in queue:
        left_result = __create_settlement_groups_recursively(receivable_amounts=sub_group_left)
        right_result = __create_settlement_groups_recursively(receivable_amounts=sub_group_right)

        candidates.append(
            [
                *left_result,
                *right_result,
            ]
        )

    # 候補の中で最も分割数が多いものを返す
    if len(candidates) > 0:
        max_candidate = max(candidates, key=len)
        __create_settlement_groups_recursively_memo[memo_key] = max_candidate
        return max_candidate

    result = [[person for person in receivable_amounts]]
    __create_settlement_groups_recursively_memo[memo_key] = result
    return result


def __create_settlements_greedy(*, receivable_amounts: dict[schemas.Person, Fraction]) -> list[schemas.Settlement]:
    settlements = []

    while True:
        person_with_max_receivable_amount = max(receivable_amounts, key=lambda person: receivable_amounts[person])
        person_with_min_receivable_amount = min(receivable_amounts, key=lambda person: receivable_amounts[person])

        if receivable_amounts[person_with_max_receivable_amount] < Fraction(1):
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
