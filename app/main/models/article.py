from dataclasses import dataclass
from sqlalchemy import Column, String, DateTime, event, Text, ForeignKey, DECIMAL, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .db.base_class import Base
from sqlalchemy.ext.hybrid import hybrid_property

# Association table for the many-to-many relationship between Article and ArticleFile
# article_files = Table('article_files', Base.metadata,
#
#                       )


@dataclass
class Article(Base):
    """
     Article model for storing user-related details, I want to create the products.
    """

    __tablename__ = 'articles'

    uuid: str = Column(String(255), primary_key=True, unique=True)
    name: str = Column(String(255), nullable=False, index=True)
    price: float = Column(DECIMAL, nullable=False, index=True)
    description: str = Column(Text, nullable=True, index=True)

    date_added: datetime = Column(DateTime, nullable=False, default=datetime.now())
    date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now())

    images = relationship("ArticleFile", backref="article")


@event.listens_for(Article, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the creation/modified field accordingly."""
    target.date_added = datetime.now()
    target.date_modified = datetime.now()


@event.listens_for(Article, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
    target.date_modified = datetime.now()


@dataclass
class ArticleFile(Base):
    """
    ArticleFile model for storing images related to articles.
    """

    __tablename__ = 'articles_files'

    article_uuid = Column(String, ForeignKey('articles.uuid', ondelete="CASCADE"), nullable=False)
    storage_uuid = Column(String, nullable=False)


