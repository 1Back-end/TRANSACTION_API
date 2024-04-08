from datetime import datetime
from typing import Any
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: Any
    code: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    uuid: str
    date_added: datetime
    date_modified: datetime

    class Config:
        orm_mode = True


class RoleDetail(Role):
    pass
