from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .user import UserBase
from .order_product import OrderProductBase, OrderProductCreate, OrderProduct
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


class OrderCreate(BaseModel):
    order_products: list[OrderProductCreate]


class OrderUpdate(OrderBase):
    pass


class Order(OrderBase):
    uuid: str
    user: UserBase
    order_products: list[OrderProductBase]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderDetail(Order):
    pass


class User(BaseModel):
    first_name: str
    last_name: str

class OrderToDisplay(BaseModel):
    uuid: str
    total_price: float
    total_price: float
    status: OrderStatusType
    order_products: list[OrderProduct]


class DisplayOrder(BaseModel):
    order: OrderToDisplay
    user: User