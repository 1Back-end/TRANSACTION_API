from datetime import datetime
from pydantic import BaseModel, ConfigDict

from .storage import Storage
from .user import UserCreate, Buyer
from .order_product import OrderProductBase, OrderProductCreate, OrderProduct
from enum import Enum
from typing import Optional, List, Any

from ..services import auth


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


class Order(OrderBase):
    uuid: str
    user: UserCreate
    order_products: list[OrderProductBase]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


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
    user: UserCreate


class OrderDetail(DisplayOrder):
    buyer: Buyer | None = None
    model_config = ConfigDict(from_attributes=True)


class ImageResponse(BaseModel):
    url: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ArticleResponse(BaseModel):
    uuid: str
    name: str
    price: float
    description: str
    images: List[ImageResponse]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderProductResponse(BaseModel):
    uuid: str
    date_added: datetime
    date_modified: datetime
    article: ArticleResponse
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    uuid: str
    code: str
    total_quantity: int
    total_price: float
    status: str
    buyer_uuid: Optional[str]
    buyer: Optional[Buyer] = None
    user_uuid: str
    user: Optional[UserCreate] = None
    order_products: list[OrderProductResponse]
    model_config = ConfigDict(from_attributes=True)


class OrderResponseList(BaseModel):
    total: int = 0
    pages: int
    current_page: int
    per_page: int
    orders: list[OrderResponse]
