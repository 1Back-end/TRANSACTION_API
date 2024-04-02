from fastapi import APIRouter

from .transaction_controller import router as transaction

api_router = APIRouter()

api_router.include_router(transaction)
