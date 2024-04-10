from sqlalchemy.orm import Session
from app.main import models , schemas
from fastapi import HTTPException, status

def get_article(db:Session , uuid:str):
    return db.query(models.Article).filter(models.Article.uuid == uuid).first()


def get_all_article(db:Session , skip : int = 0 , limit : int = 100):
    return db.query(models.Article).skip(skip).limit(limit).all()


def create_article(db:Session , article : schemas.ArticleCreate) -> schemas.Article:
     uuid=str(uuid.uuid4())
     db_article = models.Article(**article.dict(),uuid=uuid)
     db.add(db_article)
     db.commit()
     db.refresh(db_article)
     return  db_article
 



def update_article(db: Session, article: schemas.ArticleUpdate, uuid: str) -> schemas.Article:
    db_article = get_article(db, uuid)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    for key, value in article.dict(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article



def delete_article(db: Session, article: models.Article) -> None:
    db.delete(article)
    db.commit()
   
    
    
    

