from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)


class RoleDetail(Role):
    pass
