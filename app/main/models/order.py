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
    total_quantity: Integer = Column(Integer, nullable=False, index=True)
    total_price: float = Column(Float, nullable=False, index=True)
    status = Column(types.Enum(OrderStatusType), index=True, nullable=False, default=OrderStatusType.PENDING)

    articles: any = relationship("OrderProduct", backref="orders")

    user_uuid = Column(String, ForeignKey('users.uuid', ondelete="CASCADE"), nullable=True)
    user = relationship("User", foreign_keys=[user_uuid])

    date_added: any = Column(DateTime(timezone=True), default=datetime.now())
    date_modified: any = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return '<Order: uuid: {}>'.format(self.uuid)
