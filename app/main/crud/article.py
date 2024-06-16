from sqlalchemy.orm import Session
from app.main import models, schemas
from fastapi import HTTPException, status
import uuid
from app.main.services import auth, storage


def get_article(db: Session, uuid: str):
    return db.query(models.Article).filter(models.Article.uuid == uuid).first()


def get_all_article(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).skip(skip).limit(limit).all()


def create_article(db: Session, articles: list[schemas.ArticleCreate], token: str) -> list[schemas.Article]:
    valid_token = auth.get_auth_token(token=token)
    if valid_token:
        for article in articles:
            db_storage = storage.get_storage_uuid(article_storage_uuids=article.storage_uuid)
            if not db_storage:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
            if len(db_storage) != len(article.storage_uuid):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        created_articles = []
        for article in articles:
            db_article = models.Article(
                uuid=str(uuid.uuid4()),
                name=article.name,
                price=article.price,
                description=article.description)
            db.add(db_article)
            db.flush()
            for storage_uuid in article.storage_uuid:
                article_file = models.ArticleFile(
                    uuid=str(uuid.uuid4()),
                    article_uuid=db_article.uuid,
                    storage_uuid=storage_uuid
                )
                db.add(article_file)
            created_articles.append(db_article)
            db.refresh(db_article)
            print('=========created-article==========',created_articles)
        db.commit()

        return created_articles
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="token is not valid")


def update_article(db: Session, article: schemas.ArticleUpdate, uuid: str) -> schemas.Article:
    db_article = get_article(db, uuid)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article: models.Article) -> None:
    db.delete(article)
    db.commit()
