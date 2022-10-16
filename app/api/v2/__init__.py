from fastapi import APIRouter
from .endpoints import sgtv, more

v2 = APIRouter()

v2.include_router(sgtv)
v2.include_router(more)
