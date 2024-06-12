from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, String, types, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .db.base_class import Base


class OrderStatusType(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


@dataclass
class Order(Base):
    """Order model for storing order-related details, I want to create the order."""
    __tablename__ = 'orders'
    uuid: str = Column(String(255), primary_key=True, unique=True)
    total_quantity: int = Column(Integer, nullable=False, index=True)
    total_price: float = Column(Float, nullable=False, index=True)
    code: str = Column(String(5), nullable=True, default="")
    status = Column(types.Enum(OrderStatusType), index=True, nullable=False, default=OrderStatusType.PENDING)

    order_products: any = relationship("OrderProduct", back_populates="order")

    user_uuid: str = Column(String,nullable=True)
    buyer_uuid: str = Column(String, ForeignKey('buyer_info.uuid', ondelete="CASCADE"), nullable=True)
    buyer: str = relationship("BuyerInfo", foreign_keys=[buyer_uuid],   uselist= False, backref="orders")

    date_added: any = Column(DateTime(timezone=True), default=datetime.now())
    date_modified: any = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return '<Order: uuid: {}>'.format(self.uuid)
