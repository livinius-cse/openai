import logging
from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.news_article import NewsArticle
from app.schemas.news import IngestionResult, NormalizedArticle
from app.services.news_providers import GdeltClient, NEWSAPI_CATEGORIES, NewsApiClient, ReliefWebClient

logger = logging.getLogger(__name__)


class NewsIngestionService:
    """Collects, normalizes, and persists trusted-source news without AI analysis."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.settings = get_settings()

    def store(self, article: NormalizedArticle) -> bool:
        existing = self.db.scalar(select(NewsArticle).where(NewsArticle.source_url == str(article.source_url)))
        if existing:
            return False
        self.db.add(NewsArticle(title=article.title, source_url=str(article.source_url), source_name=article.source_name, provider=article.provider, category=article.category, external_id=article.external_id, content=article.content, published_at=article.published_at, raw_payload=article.raw_payload))
        self.db.commit()
        return True

    def _ingest(self, provider: str, fetch: Callable[[], list[NormalizedArticle]]) -> IngestionResult:
        try:
            articles = fetch()
            stored = sum(self.store(article) for article in articles)
            return IngestionResult(provider=provider, received=len(articles), stored=stored, skipped=not articles and provider == "newsapi" and not self.settings.newsapi_key)
        except Exception as error:
            logger.exception("%s ingestion failed", provider)
            self.db.rollback()
            return IngestionResult(provider=provider, received=0, stored=0, message=str(error))

    def ingest_all(self) -> list[IngestionResult]:
        results = []
        newsapi = NewsApiClient(self.settings.newsapi_key)
        for category in NEWSAPI_CATEGORIES:
            results.append(self._ingest("newsapi", lambda category=category: newsapi.fetch(category)))
        gdelt = GdeltClient()
        for category in NEWSAPI_CATEGORIES:
            results.append(self._ingest("gdelt", lambda category=category: gdelt.fetch(category)))
        results.append(self._ingest("reliefweb", ReliefWebClient().fetch))
        return results
