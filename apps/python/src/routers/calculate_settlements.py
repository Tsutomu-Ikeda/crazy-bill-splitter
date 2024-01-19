from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

import services
import schemas

router = APIRouter()


class CalculateSettlementRequestBody(BaseModel):
    participants: list[schemas.Person] = Field(..., min_length=1)
    payments: list[schemas.Payment] = Field(..., min_length=1)
    constraints: list[schemas.Constraint] = Field(default=[])


class CalculateSettlementResponseBody(BaseModel):
    settlements: list[schemas.Settlement] = Field(...)


@router.post("/calculate-settlements", response_model=CalculateSettlementResponseBody)
def calculate_settlements(
    body: CalculateSettlementRequestBody
) -> CalculateSettlementResponseBody:
    try:
        if len(body.constraints) == 1 and body.constraints[0] == schemas.Constraint.send_once:
            settlements = services.calculate_settlements_send_once(
                payments=body.payments,
                participants=body.participants,
            )

            return CalculateSettlementResponseBody(settlements=settlements)

        settlements = services.calculate_settlements(
            payments=body.payments,
            participants=body.participants,
        )

        return CalculateSettlementResponseBody(settlements=settlements)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
