from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, String, types, DateTime, event,Integer,Text
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, date
from .db.base_class import Base


@dataclass
class Role(Base):
     """
     Role model for storing role-related details, I want to create the role.
    """
__tablename__ = 'roles'

uuid : str = Column(String(255), primary_key=True,unique=True)
name : any = Column(JSONB, nullable=False,index=True)
code : str = Column(String(255), nullable=False,index=True)
date_added : datetime = Column(DateTime, nullable=False, default=datetime.now())
date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

def __repr__(self) -> str:
        return '<Role: uuid: {} name: {}>'.format(self.uuid, self.name)


@event.listens_for(Role, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the creation/modified field accordingly."""
    target.date_added = datetime.now()
    target.date_modified = datetime.now()


@event.listens_for(Role, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
    target.date_modified = datetime.now()
