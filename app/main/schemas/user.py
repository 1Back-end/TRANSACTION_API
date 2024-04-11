from datetime import datetime, date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserRoleBase(BaseModel):
    user_uuid: str
    role_uuid: str


class UserRoleCreate(UserRoleBase):
    pass


class UserRole(UserRoleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserStatusType(str, Enum):
    ACTIVED = "ACTIVED"
    UNACTIVED = "UNACTIVED"
    DELETED = "DELETED"
    BLOCKED = "BLOCKED"


class UserBase(BaseModel):
    country_code: str
    phone_number: str
    full_phone_number: str
    first_name: str
    last_name: str
    email: str
    address: str
    birthday: Optional[date]


class UserCreate(UserBase):
    password_hash: str
    status: UserStatusType


class UserUpdate(UserBase):
    password_hash: Optional[str]
    status: Optional[UserStatusType]


class User(UserBase):
    uuid: str
    roles: Optional[UserRole] = []

    model_config = ConfigDict(from_attributes=True)


class UserDetail(User):
    otp: Optional[str]
    otp_expired_at: Optional[datetime]
    otp_password: Optional[str]
    otp_password_expired_at: Optional[datetime]
    date_added: datetime
    date_modified: datetime
