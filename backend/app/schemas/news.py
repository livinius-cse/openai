from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class NormalizedArticle(BaseModel):
    """Provider-neutral representation used by the ingestion pipeline."""

    title: str = Field(min_length=1, max_length=500)
    source_url: HttpUrl
    source_name: str | None = None
    provider: str
    category: str
    external_id: str | None = None
    content: str = ""
    published_at: datetime | None = None
    raw_payload: dict | None = None


class NewsArticleRead(BaseModel):
    id: int
    title: str
    source_url: str
    source_name: str | None
    provider: str
    category: str
    content: str
    published_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class IngestionResult(BaseModel):
    provider: str
    received: int
    stored: int
    skipped: bool = False
    message: str | None = None
