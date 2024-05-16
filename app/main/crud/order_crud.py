from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid

from app.main.core.security import decode_access_token, generate_code
from app.main.services import auth


def create_order_products(db: Session, obj_in: schemas.OrderCreate, token: str):
    valid_token = auth.get_auth_token(token=token)
    print(f"................{valid_token['sub']}")
    if valid_token is not None:

        total_order_quantity = 0
        total_order_price = 0
        articles = []
        code = generate_code(length=9)[0:5]
        for product in obj_in.order_products:
            artile = db.query(models.Article).filter(models.Article.uuid == product.article_uuid).first()
            articles.append(artile)
            total_order_quantity += product.quantity
            total_order_price += artile.price * product.quantity
        order = models.Order(uuid=str(uuid.uuid4()), user_uuid=valid_token['sub'], total_quantity=total_order_quantity,
                             total_price=total_order_price, code=code)
        db.add(order)
        db.flush()
        index = 0
        for product in obj_in.order_products:
            artile = articles[index]
            db_obj = models.OrderProduct(
                uuid=str(uuid.uuid4()),
                price=artile.price,
                quantity=product.quantity,
                article_uuid=product.article_uuid,
                order_uuid=order.uuid,
            )
            db.add(db_obj)
            db.flush()
            db.refresh(db_obj)
            index += 1
        db.commit()
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")


def get_order_products(db: Session, token: str, code: str, uuid: str):
    valid_token = auth.get_auth_token(token=token)
    if valid_token is not None:
        user = auth.get_user(token=token, uuid=uuid)
        order: models.Order = db.query(models.Order).filter(models.Order.code == code).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this code is not valid")
        return order, user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")
