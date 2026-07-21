from datetime import datetime

from sqlalchemy import DateTime, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    source_url: Mapped[str] = mapped_column(String(2048), unique=True)
    source_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider: Mapped[str] = mapped_column(String(50), index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    external_id: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    raw_payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    problems: Mapped[list["EngineeringProblem"]] = relationship(back_populates="news_article")
