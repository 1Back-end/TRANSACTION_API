from fastapi import APIRouter

from .transaction_controller import router as transaction
from .storage_controller import router as storages

api_router = APIRouter()

api_router.include_router(transaction)
api_router.include_router(storages)
