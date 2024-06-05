from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .article import Article
from ..models import OrderStatusType


class OrderBase(BaseModel):
    total_quantity: int
    total_price: float
    status: OrderStatusType
    user_uuid: str


class OrderProductBase(BaseModel):
    quantity: int
    article_uuid: str


class OrderProductCreate(OrderProductBase):
    pass


class OrderProduct(OrderProductBase):
    uuid: str
    article: Optional[Article] = None
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)
