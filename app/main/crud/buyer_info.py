from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from typing import Any
from app.main.services import auth


def create_buyer(db: Session, obj_in: schemas.BuyerCreate, token: str, order: models.Order) -> Any:
    buyer_obj = auth.get_buyer_uuid(token=token, phone_number=obj_in.phone)
    if not buyer_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You cannot use your number to create a buyer")
    buyer: models.BuyerInfo = db.query(models.BuyerInfo).filter(models.BuyerInfo.uuid == buyer_obj).first()
    if buyer:
        buyer.name = obj_in.name
        buyer.address = obj_in.address
        buyer.email = obj_in.email
        order.buyer_uuid = buyer.uuid
        db.commit()
        return {"message": "The {} information has been updated.".format(obj_in.name)}

    db_obj = models.BuyerInfo(
                  uuid=buyer_obj,
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
