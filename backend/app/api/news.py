from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import Select, desc, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.news_article import NewsArticle
from app.schemas.news import NewsArticleRead

router = APIRouter(prefix="/news", tags=["live news"])


def article_query() -> Select[tuple[NewsArticle]]:
    return select(NewsArticle).order_by(desc(NewsArticle.published_at), desc(NewsArticle.created_at))


@router.get("", response_model=list[NewsArticleRead], summary="List ingested news")
def list_news(limit: int = Query(default=50, ge=1, le=100), db: Session = Depends(get_db)) -> list[NewsArticle]:
    """Return normalized articles from NewsAPI, GDELT, and ReliefWeb."""
    return list(db.scalars(article_query().limit(limit)))


@router.get("/latest", response_model=list[NewsArticleRead], summary="Get the latest news")
def latest_news(limit: int = Query(default=20, ge=1, le=100), db: Session = Depends(get_db)) -> list[NewsArticle]:
    return list(db.scalars(article_query().limit(limit)))


@router.get("/search", response_model=list[NewsArticleRead], summary="Search normalized news")
def search_news(q: str = Query(min_length=2, max_length=200), limit: int = Query(default=50, ge=1, le=100), db: Session = Depends(get_db)) -> list[NewsArticle]:
    pattern = f"%{q}%"
    query = article_query().where(NewsArticle.title.ilike(pattern) | NewsArticle.content.ilike(pattern)).limit(limit)
    return list(db.scalars(query))


@router.get("/category/{category}", response_model=list[NewsArticleRead], summary="Filter news by category")
def news_by_category(category: str, limit: int = Query(default=50, ge=1, le=100), db: Session = Depends(get_db)) -> list[NewsArticle]:
    articles = list(db.scalars(article_query().where(NewsArticle.category.ilike(category)).limit(limit)))
    if not articles:
        # Keep a successful empty response for a valid category without conflating it with a bad route.
        return []
    return articles
