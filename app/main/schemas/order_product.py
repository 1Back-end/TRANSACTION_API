from datetime import datetime
from pydantic import BaseModel
from .article import ArticleBase
from .order import OrderBase


class OrderProductBase(BaseModel):
    price: float
    quantity: int
    total_price: float
    article_uuid: str
    order_uuid: str


class OrderProductCreate(OrderProductBase):
    pass


class OrderProductUpdate(OrderProductBase):
    pass


class OrderProduct(OrderProductBase):
    uuid: str
    article: ArticleBase
    order: OrderBase
    date_added: datetime
    date_modified: datetime

    class Config:
        orm_mode = True


class OrderProductDetail(OrderProduct):
    pass
