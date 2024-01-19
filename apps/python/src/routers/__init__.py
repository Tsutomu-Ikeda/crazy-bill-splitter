from . import calculate_settlements

__all__ = ["routers"]


routers = [
    calculate_settlements.router,
]
