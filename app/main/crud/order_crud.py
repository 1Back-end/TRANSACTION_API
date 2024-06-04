import math

from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from sqlalchemy import or_
from app.main.core.security import decode_access_token, generate_code
from app.main.services import auth


def create_order_products(db: Session, obj_in: schemas.OrderCreate, token: str,    buyer_uuid:str):
    valid_token = auth.get_auth_token(token=token)
    print("=======",obj_in.dict())
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
                             total_price=total_order_price, code=code, buyer_uuid=buyer_uuid)
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


def get_order_products(
        db: Session,
        token: str,
        code: str,
):
    valid_token = auth.get_auth_token(token=token)
    if valid_token is not None:
        order = db.query(models.Order).filter(models.Order.code == code).first()
        user = auth.get_user(token=token,user_uuid= order.user_uuid)

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this code is not valid")

        return {"order": order, "user": user}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")

def get_order_with_pagination(
        db: Session,
        token: str,
        order: str = None,
        order_type: str = None, # "selled", "buyed"
        order_status: str = None,
        page: int = 1,
        per_page: int = 30
):

    valid_token = auth.get_auth_token(token=token)
    orders =[]
    if valid_token is not None:
        orders = db.query(models.Order)

        orders = db.query(models.Order).\
            filter(
                or_(
                        models.Order.user_uuid == decode_access_token(token)['sub'],
                        models.Order.buyer_uuid == decode_access_token(token)['sub'],
                )
        )
        print(orders)
        if not order:
            order ="ASC"

        if order_type and order_type == 'SELLED':
            orders =orders.filter(models.Order.user_uuid == decode_access_token(token)['sub'])

        if order_type and order_type == 'BUYED':
            orders =orders.filter(models.Order.buyer_uuid == decode_access_token(token)['sub'])

        if order_status and order_status == 'PAID':
            orders =orders.filter(models.Order.status == "PAID")

        if  order_status and order_status == 'CANCELLED':
            orders =orders.filter(models.Order.status == "CANCELLED")

        if order_status and order_status == 'PENDING':
            orders =orders.filter(models.Order.status == "PENDING")

        orders= orders.order_by(getattr(models.Order,"date_added" ,str(order).lower()))

        total = orders.count()
        orders =orders.offset((page - 1) * per_page).limit(per_page).all()

        return schemas.DataList(
             total = total,
            pages=math.ceil(total / per_page),
            current_page=page,
            per_page=per_page,
            data=orders
        )

def get_order_with_uuid(
        db: Session,
        token: str,
        order_uuid: str,
):
    valid_token = auth.get_auth_token(token=token)
    if valid_token is not None:
        order = db.query(models.Order).filter(models.Order.uuid == order_uuid).first()
        user = auth.get_user(token=token,user_uuid= decode_access_token(token)['sub'])
        buyer:models.BuyerInfo = order.buyer
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
        return {"order": order, "user": user,"buyer":buyer}

