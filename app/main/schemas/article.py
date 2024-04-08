from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ArticleBase(BaseModel):
    name: str
    price: float
    description: str
    storage_uuid: str


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    storage_uuid: Optional[str] = None


class Article(ArticleBase):
    date_added: datetime
    date_modified: datetime

    class Config:
        orm_mode = True


class ArticleDetail(Article):
    uuid: str
