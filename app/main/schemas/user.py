from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    country_code: str
    phone_number: str
    full_phone_number: str
    first_name: str
    last_name: str
    email: str
    address: str

