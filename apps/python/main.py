import asyncio
from typing import Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from routers import routers


app = FastAPI()

for router in routers:
    app.include_router(router)
