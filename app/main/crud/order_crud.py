import math

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from sqlalchemy import or_, and_
from app.main.core.security import decode_access_token, generate_code
from app.main.services import auth, storage
from app.main.models.order import OrderStatusType


def create_order_products(db: Session, obj_in: schemas.OrderCreate, token: str):
    valid_token = auth.get_auth_token(token=token)
    print("=======", obj_in.dict())
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


def get_order_products(
        db: Session,
        token: str,
        code: str,
):
    valid_token = auth.get_auth_token(token=token)
    if valid_token is not None:
        order: models.Order = db.query(models.Order, ).filter(models.Order.code == code).first()

        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This code is not valid")

        storage_uuids = [image.storage_uuid for order_product in order.order_products for image in
                         order_product.article.images]

        user = auth.get_user(token=token, user_uuid=order.user_uuid)
        print(f".........................user:{user}")
        storages = storage.get_storages(storage_uuids=storage_uuids)
        # print(f"....................order:{order.order_products}")
        for order_product in order.order_products:
            article_storages = []
            for article_file in order_product.article.images:
                for image in storages:
                    if image["uuid"] == article_file.storage_uuid:
                        article_storages.append(image)
            order_product.article.storages = article_storages

        return {"order": order, "user": user}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")


def get_order_with_pagination(
        db: Session,
        token: str,
        order: str = None,
        order_type: str = None,  # "selled", "buyed"
        order_status: str = None,
        page: int = 1,
        per_page: int = 30
):
    valid_token = auth.get_auth_token(token=token)
    obj = []
    if not valid_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    orders = db.query(models.Order). \
        filter(
        and_(
            models.Order.buyer_uuid != None,
            or_(
                models.Order.user_uuid == decode_access_token(token)['sub'],
                models.Order.buyer_uuid == decode_access_token(token)['sub'],
            )
        )

    )
    print(orders)
    if order_type and order_type == 'SELLED':
        orders = orders.filter(and_(models.Order.user_uuid == decode_access_token(token)['sub'], models.Order.buyer_uuid != None))

    if order_type and order_type == 'BUYED':
        orders = orders.filter(and_(models.Order.buyer_uuid == decode_access_token(token)['sub'], models.Order.buyer_uuid != None))

    if order_status and order_status == OrderStatusType.PAID:
        orders = orders.filter(and_(models.Order.status == OrderStatusType.PAID, models.Order.buyer_uuid != None))

    if order_status and order_status == OrderStatusType.CANCELLED:
        orders = orders.filter(and_(models.Order.status == OrderStatusType.CANCELLED, models.Order.buyer_uuid != None))

    if order_status and order_status == OrderStatusType.PENDING:
        orders = orders.filter(and_(models.Order.status == OrderStatusType.PENDING, models.Order.status == OrderStatusType.PENDING))

    if order and order.lower() == "asc":
        orders = orders.order_by(getattr(models.Order, "date_added").asc())

    if order and order.lower() == "desc":
        orders = orders.order_by(getattr(models.Order, "date_added").desc())

    total = orders.count()
    orders = orders.offset((page - 1) * per_page).limit(per_page).all()
    for order in orders:
        userId = decode_access_token(token)['sub']
        print(f".............command uuid:{order.uuid}")
        print(f".............buyer uuid frere{order.buyer_uuid}")
        second_user_id: str = order.user_uuid if order.buyer_uuid == userId else order.buyer_uuid
        print("........first: {}, second: {}".format(userId, second_user_id))
        users = auth.get_users(token=token, uuid=second_user_id)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        storage_uuids = [image.storage_uuid for order_product in order.order_products for image in
                         order_product.article.images]
        storages = storage.get_storages(storage_uuids=storage_uuids)
        # print(f"....................order:{order.order_products}")
        for order_product in order.order_products:
            article_storages = []
            for article_file in order_product.article.images:
                for image in storages:
                    if image["uuid"] == article_file.storage_uuid:
                        article_storages.append(image)
            order_product.article.storages = article_storages

        obj.append({
            "order": order,
            "user": users[0 if userId == order.user_uuid else 1],
            "buyer": users[1 if userId == order.user_uuid else 0],
        })
    print(f"....................the value of data in datalist:{obj}")

    return schemas.DataList(
        total=total,
        pages=math.ceil(total / per_page),
        current_page=page,
        per_page=per_page,
        data=obj
    )


def get_order_with_uuid(
        db: Session,
        token: str,
        order_uuid: str,
):
    valid_token = auth.get_auth_token(token=token)
    if not valid_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not valid")
    order = db.query(models.Order).filter(models.Order.uuid == order_uuid).first()
    userId = decode_access_token(token)['sub']
    print(f".............command uuid:{order.uuid}")
    print(f".............buyer uuid frere{order.buyer_uuid}")
    second_user_id: str = order.user_uuid if order.buyer_uuid == userId else order.buyer_uuid
    print("........first: {}, second: {}".format(userId, second_user_id))
    users = auth.get_users(token=token, uuid=second_user_id)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return {"order": order,
            "user": users[0 if userId == order.user_uuid else 1],
            "buyer": users[1 if userId == order.user_uuid else 0]}


def mark_order_as_cancelled(
        *,
        db: Session,
        order: models.Order = None,
):
    order.status = OrderStatusType.CANCELLED
    db.commit()
