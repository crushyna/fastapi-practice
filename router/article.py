from auth.oauth2 import oauth2_scheme, get_current_user
from schemas import ArticleBase, ArticleDisplay, UserBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_article

router = APIRouter(
    prefix='/article',
    tags=['user']
)


# Create article
@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db),
                   current_user: UserBase = Depends(get_current_user)):
    return db_article.create_article(db, request)


# Get Specific article
@router.get('/{id}')
def get_article(id: int, db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.get_article(db, id),
        'current_user': current_user
    }
