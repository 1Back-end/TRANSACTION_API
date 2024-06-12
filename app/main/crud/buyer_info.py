from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from typing import Any
from app.main.services import auth


def create_buyer(db: Session, obj_in: schemas.BuyerCreate, token: str, order: models.Order,) -> Any:

    buyer_obj = auth.get_buyer_uuid(token=token, phone_number=obj_in.phone)
    if buyer_obj:
        if db.query(models.BuyerInfo).filter(models.BuyerInfo.uuid == buyer_obj.get("uuid")).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="This buyer is already registered")
        db_obj = models.BuyerInfo(
            uuid=buyer_obj.get("full_phone_number"),
            name=obj_in.name,
            email=obj_in.email,
            phone=obj_in.phone,
            address=obj_in.address
        )
        db.add(db_obj)
        db.flush()

        order.buyer_uuid = db_obj.uuid
        db.commit()
        db.refresh(db_obj)
        return db_obj
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")
