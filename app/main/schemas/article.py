from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    name: str
    price: float
    description: str | None = None
    storage_uuid: List[str] | None = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    storage_uuid: Optional[List[str]] = None


class Storage(BaseModel):
    url: str


class Image(BaseModel):
    url: Optional[str]


class Article(ArticleBase):
    uuid: str
    name: str
    price: float
    description: str | None = None
    images: List[Image]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleDetail(Article):
    uuid: str
