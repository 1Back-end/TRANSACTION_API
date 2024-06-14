from pydantic import BaseModel


class Storage(BaseModel):
    uuid: str
    url: str
