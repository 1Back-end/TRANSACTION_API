import math

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from sqlalchemy import or_
from app.main.core.security import decode_access_token, generate_code
from app.main.services import auth
from  app.main.models.order import  OrderStatusType

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
        user = auth.get_user(token=token,user_uuid=order.user_uuid)

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
            orders = orders.filter(models.Order.user_uuid == decode_access_token(token)['sub'])

        if order_type and order_type == 'BUYED':
            orders = orders.filter(models.Order.buyer_uuid == decode_access_token(token)['sub'])

        if order_status and order_status == OrderStatusType.PAID:
            orders =orders.filter(models.Order.status == OrderStatusType.PAID)

        if  order_status and order_status == OrderStatusType.CANCELLED:
            orders =orders.filter(models.Order.status == OrderStatusType.CANCELLED)

        if order_status and order_status == OrderStatusType.PENDING:
            orders =orders.filter(models.Order.status == OrderStatusType.PENDING)

        orders= orders.order_by(getattr(models.Order,"date_added" ,str(order).lower()))

        total = orders.count()
        orders = orders.offset((page - 1) * per_page).limit(per_page).all()

        data = jsonable_encoder(orders)
        for order in data:
            user = auth.get_user(token = token,user_uuid =order["user_uuid"])
            order["user"] = schemas.UserCreate(
                country_code =user["country_code"],
                phone_number =user["phone_number"],
                full_phone_number =user["full_phone_number"],
                first_name = user["first_name"],
                last_name = user["last_name"],
                email = user["email"],
                address = user["address"]
            )

        # return\
        #     {
        #     "total": total,
        #     "pages": math.ceil(total / per_page),
        #     "current_page": page,
        #     "per_page": per_page,
        #     "data": [
        #             {
        #                 "uuid": order.uuid,
        #                 "code": order.code,
        #                 "total_quantity": order.total_quantity,
        #                 "total_price": order.total_price,
        #                 "date_added": order.date_added,
        #                 "status": order.status,
        #                 "buyer_uuid": order.buyer_uuid,
        #                 "buyer": order.buyer,
        #                 "user_uuid": order.user_uuid,
        #                 "user": auth.get_user(token = token,user_uuid =order.user_uuid),
        #
        #                 "order_products": [
        #                     {
        #                         "uuid": order_product.uuid,
        #                         "price": order_product.price,
        #                         "quantity": order_product.quantity,
        #                         "article_uuid": order_product.article_uuid,
        #                         "article":{
        #                             "uuid": order_product.article.uuid,
        #                             "name": order_product.article.name,
        #                             "price": order_product.article.price,
        #                             "description": order_product.article.description,
        #                             "date_added": order_product.article.date_added,
        #                             "images": [
        #                                 {
        #                                     "url":article.url
        #                                 }
        #
        #                             for article in order_product.article.images
        #                             ]
        #                              },
        #                         "order_uuid": order_product.order_uuid,
        #                     }
        #                     for order_product in order.order_products
        #                 ]
        #             }
        #             for order in orders
        #     ]
        # }

        return schemas.DataList(
            total = total,
            pages = math.ceil(total/per_page),
            current_page =  page,
            per_page = per_page,
            data = data
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


def mark_order_as_cancelled(
        *,
        db: Session,
        order: models.Order = None,
):
    order.status = OrderStatusType.CANCELLED
    db.commit()
