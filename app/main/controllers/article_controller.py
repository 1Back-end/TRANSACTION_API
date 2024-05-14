from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.main import models, schemas
from app.main.core.dependencies import get_db
from app.main.crud.article import create_article

router = APIRouter(prefix="/article", tags=["article"])


@router.post("/{token}")
def articles(article: schemas.ArticleCreate, token: str, db: Session = Depends(get_db)):
    try:
        db_article = create_article(db=db, article=article, token=token)
        return {"message": "Article created successfully", "article": db_article}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{uuid}", response_model=schemas.Article)
def get_article(uuid: str, db: Session = Depends(get_db)):
    db_article = get_article(db=db, uuid=uuid)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article


@router.get("/articles", response_model=list[schemas.Article])
def get_all_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles


@router.put("/{uuid}", response_model=schemas.Article)
def update_article(uuid: str, article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    try:
        updated_article = update_article(db=db, article=article, uuid=uuid)
        return updated_article
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/article/{uuid}")
def delete_article(uuid: str, db: Session = Depends(get_db)):
    try:
        db_article = get_article(db=db, uuid=uuid)
        if db_article is None:
            raise HTTPException(status_code=404, detail="Article not found")
        delete_article(db=db, article=db_article)
        return {"message": "Article deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
