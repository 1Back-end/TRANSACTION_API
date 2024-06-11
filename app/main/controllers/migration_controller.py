import json
import os
import shutil
import platform
from dataclasses import dataclass
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import Column, String
from app.main import schemas, models
from app.main.core.config import Config
from app.main.core import dependencies
from app.main.models.db.base_class import Base
from app.main.utils import logger
from app.main import crud

router = APIRouter(prefix="/migrations", tags=["migrations"])


def check_user_access_key(admin_key: schemas.AdminKey):
    logger.info(f"Check user access key: {admin_key.key}")
    if admin_key.key not in [Config.ADMIN_KEY]:
        raise HTTPException(status_code=400, detail="Clé d'accès incorrecte")


@router.post("/create-database-tables", response_model=schemas.Msg, status_code=201)
async def create_database_tables(
        db: Session = Depends(dependencies.get_db),
        admin_key: schemas.AdminKey = Body(...)
) -> dict[str, str]:
    """
    Create database structure (tables)
    """
    check_user_access_key(admin_key)
    """ Try to remove previous alembic tags in database """
    try:
        @dataclass
        class AlembicVersion(Base):
            __tablename__ = "alembic_version"
            version_num: str = Column(String(32), primary_key=True, unique=True)

        db.query(AlembicVersion).first().delete()
        db.commit()
    except Exception as e:
        pass

    """ Try to remove previous alembic versions folder """
    migrations_folder = os.path.join(os.getcwd(), "alembic", "versions")
    try:
        shutil.rmtree(migrations_folder)
    except Exception as e:
        pass

    """ create alembic versions folder content """
    try:
        os.mkdir(migrations_folder)
    except OSError:
        logger.error("Creation of the directory %s failed" % migrations_folder)
    else:
        logger.error("Successfully created the directory %s " % migrations_folder)

    try:
        # Get the environment system
        if platform.system() == 'Windows':

            os.system('set PYTHONPATH=. && .\\.venv\Scripts\python.exe -m alembic revision --autogenerate')

        else:
            os.system('PYTHONPATH=. alembic revision --autogenerate')

        # Get the environment system
        if platform.system() == 'Windows':

            os.system('set PYTHONPATH=. && .\\.venv\Scripts\python.exe -m alembic upgrade head')

        else:
            os.system('PYTHONPATH=. alembic upgrade head')

        """ Try to remove previous alembic versions folder """
        try:
            shutil.rmtree(migrations_folder)
            pass
        except Exception as e:
            pass

        return {"message": "Les tables de base de données ont été créées avec succès"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create-storages", response_model=schemas.Msg, status_code=201)
def create_storages(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default sstorages
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/storages.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                storage = crud.file_storage.get(db=db, uuid = data["uuid"])
                if not storage:
                    storage = models.Storage(
                        uuid = data["uuid"],
                        file_name = data["file_name"],
                        url = data["url"],
                        mimetype = data["mimetype"],
                        width = data["width"],
                        height = data["height"],
                        size = data["size"],
                        thumbnail = data["thumbnail"],
                        medium = data["medium"],
                        date_added = data["date_added"],
                        date_modified = data["date_modified"]

                    )
                    db.add(storage)
                    db.commit()
                    db.refresh(storage)
        return {"message": "storage created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")


@router.post("/create-orders", response_model=schemas.Msg, status_code=201)
def create_orders(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default orders
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/orders.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                order = db.query(models.Order).filter(models.Order.uuid == data["uuid"]).first()
                if not order:
                    order = models.Order(
                        uuid = data["uuid"],
                        user_uuid = data["user_uuid"],
                        total_quantity = data["total_quantity"],
                        total_price = data["total_price"],
                        status = data["status"],
                        date_added = data["date_added"],
                        date_modified = data["date_modified"],
                        code = data["code"],
                        buyer_uuid = data["buyer_uuid"]
                    )
                    db.add(order)
                    db.commit()
                    db.refresh(order)
        return {"message": "orders created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")


@router.post("/create-order-products", response_model=schemas.Msg, status_code=201)
def create_order_products(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default order products
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/order_products.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                order_product = db.query(models.OrderProduct).filter(models.OrderProduct.uuid == data["uuid"]).first()
                if not order_product:
                    order_product = models.OrderProduct(
                        uuid = data["uuid"],
                        price = data["price"],
                        quantity = data["quantity"],
                        total_price= data["total_price"],
                        article_uuid = data["article_uuid"],
                        order_uuid = data["order_uuid"],
                        date_added = data["date_added"],
                        date_modified = data["date_modified"]
                    )
                    db.add(order_product)
                    db.commit()
                    db.refresh(order_product)
        return {"message": "order_products created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")


@router.post("/create-buyer-infos", response_model=schemas.Msg, status_code=201)
def create_buyer_infos(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default buyer_infos
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/buyer_infos.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                buyer_info = db.query(models.BuyerInfo).filter(models.BuyerInfo.uuid == data["uuid"]).first()
                if not buyer_info:
                    buyer_info = models.BuyerInfo(
                        uuid = data["uuid"],
                        name = data["name"],
                        email = data["email"],
                        phone = data["phone"],
                        address = data["address"]
                    )
                    db.add(buyer_info)
                    db.commit()
                    db.refresh(buyer_info)
        return {"message": "buyer_infos created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")


@router.post("/create-article-files", response_model=schemas.Msg, status_code=201)
def create_article_files(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default article_files
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/article_files.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                article_file = db.query(models.ArticleFile).filter(models.ArticleFile.article_uuid == data["article_uuid"]).first()
                if not article_file:
                    article_file = models.ArticleFile(
                        article_uuid = data["article_uuid"],
                        storage_uuid = data["storage_uuid"],
                    )
                    db.add(article_file)
                    db.commit()
                    db.refresh(article_file)
        return {"message": "articles files created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")


@router.post("/create-articles", response_model=schemas.Msg, status_code=201)
def create_articles(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default articles
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/articles.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                article= db.query(models.Article).filter(models.Article.uuid == data["uuid"]).first()
                if not article:
                    article = models.Article(
                        uuid = data["uuid"],
                        name = data["name"],
                        description = data["description"],
                        price = data["price"],
                        date_added = data["date_added"],
                        date_modified = data["date_modified"]
                    )
                    db.add(article)
                    db.commit()
                    db.refresh(article)
        return {"message": "articles  created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")

def create_articles(
    db: Session = Depends(dependencies.get_db),
    admin_key: schemas.AdminKey = Body(...)
) -> Any:
    """
    Create default articles
    """
    check_user_access_key(admin_key)
    try:
        with open('{}/app/main/templates/data/articles.json'.format(os.getcwd()), encoding='utf-8') as f:
            datas = json.load(f)
            for data in datas:
                article= db.query(models.Article).filter(models.Article.uuid == data["uuid"]).first()
                if not article:
                    article = models.Article(
                        uuid = data["uuid"],
                        name = data["name"],
                        description = data["description"],
                        price = data["price"],
                        date_added = data["date_added"],
                        date_modified = data["date_modified"]
                    )
                    db.add(article)
                    db.commit()
                    db.refresh(article)
        return {"message": "articles  created successfully"}
    except IntegrityError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Erreur du serveur")