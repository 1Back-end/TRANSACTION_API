from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, String, types, DateTime, event,Integer,Text,ForeignKey,Table
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .db.base_class import Base


@dataclass
class ArticleFile(Base):

    """ Article Files Model for store all Article File """

    __tablename__ = 'articles_files'

article_uuid = Column(String, ForeignKey('articles.uuid', ondelete="CASCADE"), nullable=True)
article = relationship("Article", foreign_keys=[article_uuid])

storage_uuid = Column(String, ForeignKey('storages.uuid', ondelete="CASCADE"), nullable=True)
storage = relationship("Storage", foreign_keys=[storage_uuid])

    
@dataclass
class Article(Base):
     """
     Article model for storing user-related details, I want to create the products.
    """
__tablename__ = 'articles'

uuid : str = Column(String(255), primary_key=True,unique=True)
name : str = Column(String(255),nullable=False,index=True)
price: float = Column(float,nullable=False,index=True)
description : str = Column(Text,nullable=True,index=True)

date_added : datetime = Column(DateTime, nullable=False, default=datetime.now())
date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now())

images: any = relationship("ArticleFile",backref="storage")


def __repr__(self) -> str:
         return f"Article(uuid_article={self.uuid_article!r}, photo_article={self.photo_article!r},
     name_article={self.name_article!r},price_article={self.price_article!r},
     description_article={self.description_article!r},date_modified={self.date_modified!r})"





    
    