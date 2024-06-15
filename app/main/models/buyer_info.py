from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, String, types, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .db.base_class import Base


@dataclass
class BuyerInfo(Base):
    __tablename__ = "buyer_info"
    uuid: str = Column(String(255), primary_key=True, unique=True)
    name: str = Column(String(255), nullable=False, index=True)
    email: str = Column(String(100), nullable=True, default="", index=True)
    phone: str = Column(String(25), nullable=False, default="", index=True)
    address: str = Column(String(100), nullable=False, default="")

    def __repr__(self):
        return '<Buyer: uuid: {}>'.format(self.uuid)
