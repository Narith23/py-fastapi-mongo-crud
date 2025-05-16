# This is a sample __init__.py file
from fastapi import APIRouter

from api.router.item import router as item_router

router = APIRouter()

router.include_router(item_router)
