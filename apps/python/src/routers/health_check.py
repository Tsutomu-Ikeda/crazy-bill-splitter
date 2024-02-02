from fastapi import APIRouter

router = APIRouter()


@router.get("/health-check")
def calculate_settlements() -> str:
    return "OK"
