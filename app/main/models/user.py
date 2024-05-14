from dataclasses import dataclass
from enum import Enum
from sqlalchemy import Column, String, types, DateTime, event,Table,ForeignKey
from datetime import datetime, date
from sqlalchemy.orm import relationship
from .db.base_class import Base


    
class UserStatusType(str, Enum):
    ACTIVED = "ACTIVED"
    UNACTIVED = "UNACTIVED"
    DELETED = "DELETED"
    BLOCKED = "BLOCKED"


@dataclass
class User(Base):
    """
    User model for storing users related details
    """
    __tablename__ = 'users'

    uuid: str = Column(String, primary_key=True, unique=True)

    country_code: str = Column(String(5), nullable=False, default="", index=True)
    phone_number: str = Column(String(20), nullable=False, default="", index=True)
    full_phone_number: str = Column(String(25), nullable=False, default="", index=True)
    first_name: str = Column(String(100), nullable=False, default="")
    last_name: str = Column(String(100), nullable=False, default="")
    email: str = Column(String(100), nullable=False, default="", index=True)
    address: str = Column(String(100), nullable=False, default="")

    date_added: datetime = Column(DateTime, nullable=False, default=datetime.now())
    date_modified: datetime = Column(DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return '<User: uuid: {} full_phone_number: {}>'.format(self.uuid, self.full_phone_number)


@event.listens_for(User, 'before_insert')
def update_created_modified_on_create_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the creation/modified field accordingly."""
    target.date_added = datetime.now()
    target.date_modified = datetime.now()


@event.listens_for(User, 'before_update')
def update_modified_on_update_listener(mapper, connection, target):
    """ Event listener that runs before a record is updated, and sets the modified field accordingly."""
    target.date_modified = datetime.now()