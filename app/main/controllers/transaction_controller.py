from fastapi import APIRouter
from fastapi import Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.main import models, schemas
from app.main.core.dependencies import get_db
from app.main.crud.buyer_info import create_buyer
from app.main.crud.order_crud import create_order_products, get_order_products, get_order_with_pagination, \
    get_order_with_uuid, mark_order_as_cancelled
from app.main.core.security import decode_access_token

from app.main.services import auth

router = APIRouter(prefix="", tags=["transaction"])


@router.post("/infos_buyer/{token}")
def save_buyer_information(buyer: schemas.BuyerCreate, token: str, db: Session = Depends(get_db)):
    order: models.Order = db.query(models.Order).filter(models.Order.uuid == buyer.order_uuid).first()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    try:
        db_article = create_buyer(db=db, obj_in=buyer, token=token, order=order)
        return db_article
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error has occurred")


@router.post("/order/create/{token}")
def creat_order(order: schemas.OrderCreate, token: str, buyer_uuid: str = None, db: Session = Depends(get_db)):
    try:
        db_article = create_order_products(db=db, obj_in=order, token=token, buyer_uuid=buyer_uuid)
        return {"message": "Article created successfully", "order": db_article}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error has occurred")


@router.get("/order/get/{token}", response_model=schemas.DisplayOrder)
def get_orders(token: str,
               code: str,
               db: Session = Depends(get_db),
               ):
    try:
        orders = get_order_products(db=db, token=token, code=code)

        return orders
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@router.get("/orders/get/{token}")
def get_orders_with_pagination(
        token: str,
        order: str = Query("ASC", enum=["ASC", "DESC"]),
        order_status: str = Query(None, enum=["PAID", "PENDING", "CANCELLED"]),
        order_type: str = Query(None, enum=["SELLED", "BUYED"]),
        page: int = 1,
        per_page: int = 30,
        db: Session = Depends(get_db),
):
    try:
        orders = get_order_with_pagination(
            db=db,
            token=token,
            page=page,
            per_page=per_page,
            order=order,
            order_status=order_status,
            order_type=order_type
        )

        return orders
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@router.get("/orders/get/{token}/{order_uuid}", response_model=schemas.OrderDetail)
def get_order_by_uuid(
        token: str,
        order_uuid: str,
        db: Session = Depends(get_db),
):
    try:
        order = get_order_with_uuid(
            db=db,
            token=token,
            order_uuid=order_uuid
        )
        return order

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")


@router.put("/order/cancel/{token}")
def cancel_order(
        *,
        db: Session = Depends(get_db),
        token: str,
        order_uuid: str,
):
    order: models.Order = db.query(models.Order).filter(models.Order.uuid == order_uuid).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")

    valid_token = auth.get_auth_token(token=token)
    if not valid_token:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")

    if order.user_uuid == decode_access_token(token)['sub']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to perform this action")

    try:
        mark_order_as_cancelled(
            db=db,
            order=order,
        )
        return {"message": "order cancelled with success!"}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
