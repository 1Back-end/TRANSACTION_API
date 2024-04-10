from datetime import datetime
from pydantic import BaseModel
from .user import UserBase
from .order_product import OrderProductBase
from enum import Enum


class OrderStatusType(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class OrderBase(BaseModel):
    total_quantity: int
    total_price: float
    status: OrderStatusType
    user_uuid: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase):
    uuid: str
    user: UserBase
    order_products: list[OrderProductBase]
    date_added: datetime
    date_modified: datetime

    class Config:
        orm_mode = True


class OrderDetail(Order):
    pass
