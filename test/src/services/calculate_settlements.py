from pydantic import BaseModel, Field
import requests

import env
import schemas


class CalculateSettlementRequestBody(BaseModel):
    participants: list[schemas.Person] = Field(..., min_length=1)
    payments: list[schemas.Payment] = Field(..., min_length=1)


class CalculateSettlementResponseBody(BaseModel):
    settlements: list[schemas.Settlement] = Field(...)


def calculate_settlements(request_body: CalculateSettlementRequestBody) -> CalculateSettlementResponseBody:
    resp = requests.post(
        url=f"{env.settings.TARGET_HOST}/calculate-settlements",
        json=request_body.model_dump(),
    )

    resp.raise_for_status()

    return CalculateSettlementResponseBody(**resp.json())
