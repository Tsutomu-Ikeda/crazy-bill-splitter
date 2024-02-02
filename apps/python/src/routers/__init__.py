from . import calculate_settlements
from . import health_check

__all__ = ["routers"]


routers = [
    calculate_settlements.router,
    health_check.router,
]
