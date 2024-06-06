from pydantic import BaseModel, ConfigDict


class BuyerBase(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None


class BuyerCreate(BuyerBase):
    order_uuid: str


class Buyer(BuyerBase):
    uuid: str

    model_config = ConfigDict(from_attributes=True)


