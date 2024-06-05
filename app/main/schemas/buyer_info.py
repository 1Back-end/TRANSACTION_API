from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class BuyerBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class BuyerCreate(BuyerBase):
    order_uuid: str


class Buyer(BuyerBase):
    uuid: str

    model_config = ConfigDict(from_attributes=True)


