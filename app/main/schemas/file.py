from pydantic import BaseModel, ConfigDict
from typing import Any


class FileUpload(BaseModel):
    file_name: str | None = None
    base_64: Any | None = None


class FileResize(BaseModel):
    file_name: str | None = None
    url: str | None = None


class File(BaseModel):
    file_name: str
    url: str
    mimetype: int | None = None
    width: int | None = None
    height: int | None = None
    size: int | None = None
    thumbnail: FileResize | None = None
    medium: FileResize | None = None

    model_config = ConfigDict(from_attributes=True)
