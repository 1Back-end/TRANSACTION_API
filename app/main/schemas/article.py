from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    name: str
    price: float
    description: str | None = None
    storage_uuid: str | None = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    storage_uuid: Optional[str] = None

class Image(BaseModel):
    url : str
class Article(ArticleBase):
    name: str
    price: float
    description: str
    images : List[Image]
    date_added: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleDetail(Article):
    uuid: str
