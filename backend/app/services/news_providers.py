"""HTTP clients and normalizers for third-party news and events providers."""

import logging
from datetime import UTC, datetime
from typing import Any

import httpx

from app.schemas.news import NormalizedArticle

logger = logging.getLogger(__name__)
NEWSAPI_CATEGORIES = ("technology", "disaster", "infrastructure", "health", "climate", "public safety")


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


class NewsApiClient:
    base_url = "https://newsapi.org/v2/everything"

    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    def fetch(self, category: str, limit: int = 20) -> list[NormalizedArticle]:
        if not self.api_key:
            logger.warning("NewsAPI ingestion skipped: NEWSAPI_KEY is not configured")
            return []
        response = httpx.get(self.base_url, params={"q": category, "language": "en", "sortBy": "publishedAt", "pageSize": limit, "apiKey": self.api_key}, timeout=20)
        response.raise_for_status()
        return [self.normalize(article, category) for article in response.json().get("articles", []) if article.get("url") and article.get("title")]

    @staticmethod
    def normalize(article: dict[str, Any], category: str) -> NormalizedArticle:
        return NormalizedArticle(title=article["title"], source_url=article["url"], source_name=article.get("source", {}).get("name"), provider="newsapi", category=category, external_id=article.get("url"), content=article.get("content") or article.get("description") or "", published_at=parse_datetime(article.get("publishedAt")), raw_payload=article)


class GdeltClient:
    base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

    def fetch(self, category: str, limit: int = 20) -> list[NormalizedArticle]:
        response = httpx.get(self.base_url, params={"query": category, "mode": "artlist", "format": "json", "maxrecords": limit, "sort": "HybridRel"}, timeout=20)
        response.raise_for_status()
        return [self.normalize(article, category) for article in response.json().get("articles", []) if article.get("url") and article.get("title")]

    @staticmethod
    def normalize(article: dict[str, Any], category: str) -> NormalizedArticle:
        return NormalizedArticle(title=article["title"], source_url=article["url"], source_name=article.get("domain"), provider="gdelt", category=category, external_id=article.get("url"), content=article.get("seendate") or "", published_at=parse_datetime(article.get("seendate")), raw_payload=article)


class ReliefWebClient:
    base_url = "https://api.reliefweb.int/v1/reports"

    def fetch(self, limit: int = 20) -> list[NormalizedArticle]:
        payload = {"limit": limit, "sort": ["date.created:desc"], "fields": {"include": ["title", "url", "source", "body", "date", "id"]}, "filter": {"field": "disaster", "value": "*"}}
        response = httpx.post(self.base_url, params={"appname": "forgeai"}, json=payload, timeout=20)
        response.raise_for_status()
        return [self.normalize(item) for item in response.json().get("data", []) if item.get("fields", {}).get("url")]

    @staticmethod
    def normalize(item: dict[str, Any]) -> NormalizedArticle:
        fields = item.get("fields", {})
        source = fields.get("source") or []
        source_name = source[0].get("name") if source else "ReliefWeb"
        return NormalizedArticle(title=fields.get("title", "Untitled ReliefWeb report"), source_url=fields["url"], source_name=source_name, provider="reliefweb", category="disaster", external_id=str(item.get("id")), content=fields.get("body") or "", published_at=parse_datetime((fields.get("date") or {}).get("created")), raw_payload=item)
