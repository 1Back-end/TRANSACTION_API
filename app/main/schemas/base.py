from pydantic import BaseModel, ConfigDict
from typing import Any, List, TypeVar, Generic

T = TypeVar('T')


class DataList(BaseModel, Generic[T]):
    total: int
    pages: int
    current_page: int
    per_page: int
    data: List[T] = []

    model_config = ConfigDict(from_attributes=True)
