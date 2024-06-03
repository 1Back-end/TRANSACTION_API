from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.main import models, schemas
from app.main.core.dependencies import get_db
from app.main.crud.buyer_info import create_buyer
from app.main.crud.order_crud import create_order_products, get_order_products

router = APIRouter(prefix="", tags=["transaction"])


@router.post("/infos_buyer/{token}")
def save_buyer_information(buyer: schemas.BuyerCreate, token: str, db: Session = Depends(get_db)):
    try:
        db_article = create_buyer(db=db, obj_in=buyer, token=token)
        return {"message": "Article created successfully", "article": db_article}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error has occurred")


@router.post("/order/create/{token}")
def creat_order(order: schemas.OrderCreate, token: str, db: Session = Depends(get_db)):
    try:
        db_article = create_order_products(db=db, obj_in=order, token=token)
        return {"message": "Article created successfully", "article": db_article}
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
