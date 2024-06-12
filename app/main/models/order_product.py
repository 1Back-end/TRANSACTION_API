from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, String, types, DateTime, event, Integer, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .db.base_class import Base


@dataclass
class OrderProduct(Base):
    """ Order Products Model for store all products order """

    __tablename__ = 'order_products'

    uuid: str = Column(String, primary_key=True, unique=True)
    price: float = Column(Float, nullable=False, index=True)
    quantity: int = Column(Integer, nullable=True, default=1)
    total_price: float = Column(Float, unique=False, nullable=True, default=0)

    article_uuid: str = Column(String, ForeignKey('articles.uuid', ondelete="CASCADE"), nullable=True)
    article = relationship("Article", foreign_keys=[article_uuid])

    order_uuid: str = Column(String, ForeignKey('orders.uuid', ondelete="CASCADE"), nullable=True)
    order = relationship("Order", foreign_keys=[order_uuid], back_populates="order_products")

    date_added: any = Column(DateTime(timezone=True), default=datetime.now())
    date_modified: any = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now)

    # def __repr__(self):
    #     return '<OrderProducts: uuid: {}>'.format(self.uuid)


@event.listens_for(OrderProduct, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the creation/modified field accordingly."""
    target.date_added = datetime.now()
    target.date_modified = datetime.now()


@event.listens_for(OrderProduct, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
    target.date_modified = datetime.now()
