from fastapi import APIRouter

from .transaction_controller import router as transaction
from .article_controller import router as article

api_router = APIRouter()

api_router.include_router(transaction)
api_router.include_router(article)