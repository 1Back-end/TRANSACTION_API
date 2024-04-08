from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime,Table
from app.main.models.db.base_class import Base



@dataclass
class Storage(Base):
    
    """ Avatar Model for storing file related details in database"""

    __tablename__ = "storages"

    uuid: str = Column(String, primary_key=True, unique=True)
    file_name: str = Column(Text, default="", nullable=True)
    url: str = Column(Text, default="", nullable=True)
    mimetype: str = Column(Text, default="", nullable=True)
    width: int = Column(Integer, default=0, nullable=True)
    height:int = Column(Integer, default=0, nullable=True)
    size:int = Column(Integer, default=0, nullable=True)
    thumbnail: any = Column(JSONB, default={}, nullable=True)
    medium: any = Column(JSONB, default={}, nullable=True)
    date_added: any = Column(DateTime(timezone=True), default=datetime.now())
    date_modified: any = Column(DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now())
  
    def __repr__(self):
        return '<Storage: uuid: {} file_name: {} url: {} />'.format(self.uuid, self.file_name, self.url)

