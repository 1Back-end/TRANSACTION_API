from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from typing import Any
from app.main.services import auth


def create_buyer(db: Session, obj_in: schemas.BuyerCreate, token: str) -> Any:

    valid_token = auth.get_auth_token(token=token)
    if valid_token:
        db_obj = models.BuyerInfo(
            uuid=str(uuid.uuid4()),
            name=obj_in.name,
            email=obj_in.email,
            phone=obj_in.phone,
            address=obj_in.address
        )
        db.add(db_obj)
        db.commit()

        db.refresh(db_obj)
        return db_obj
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")
