from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from typing import Any

from app.main.core.security import decode_access_token
from app.main.services import auth


def create_buyer(db: Session, obj_in: schemas.BuyerCreate, token: str, ) -> Any:
    valid_token = auth.get_auth_token(token=token)
    if not valid_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")
    db_obj = models.BuyerInfo(
        uuid=str(uuid.uuid4()),
        name=obj_in.name,
        email=obj_in.email,
        phone=obj_in.phone,
        address=obj_in.address
    )
    db.add(db_obj)
    db.flush()
    db.commit()
    db.refresh(db_obj)
    return db_obj


def link_bayer_to_order_crud(db: Session, token: str, order_uuid: str) -> Any:
    user = auth.get_auth_token(token=token)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")
    order: models.Order = db.query(models.Order).filter(models.Order.uuid == order_uuid)\
        .filter(models.Order.buyer_uuid is None).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    if order.buyer_uuid == order.user_uuid:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="You cannot be the buyer of an order you have created.")
    order.buyer_uuid = decode_access_token(token)['sub']
    db.add(order)
    db.flush()
    db.commit()
    db.refresh(order)

