from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EngineeringProblem(Base):
    __tablename__ = "engineering_problems"

    id: Mapped[int] = mapped_column(primary_key=True)
    news_article_id: Mapped[int] = mapped_column(ForeignKey("news_articles.id"), index=True)
    title: Mapped[str] = mapped_column(String(300))
    summary: Mapped[str] = mapped_column(Text)
    sector: Mapped[str] = mapped_column(String(100), index=True)
    region: Mapped[str | None] = mapped_column(String(150), nullable=True)
    severity: Mapped[str] = mapped_column(String(30), default="medium")
    urgency_score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    news_article: Mapped["NewsArticle"] = relationship(back_populates="problems")
    recommendations: Mapped[list["TechnologyRecommendation"]] = relationship(back_populates="problem")
    innovation_gaps: Mapped[list["InnovationGap"]] = relationship(back_populates="problem")
