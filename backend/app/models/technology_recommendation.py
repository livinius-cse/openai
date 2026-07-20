from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TechnologyRecommendation(Base):
    __tablename__ = "technology_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    engineering_problem_id: Mapped[int] = mapped_column(ForeignKey("engineering_problems.id"), index=True)
    technology_name: Mapped[str] = mapped_column(String(255))
    rationale: Mapped[str] = mapped_column(Text)
    maturity_level: Mapped[str] = mapped_column(String(50))
    match_score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    problem: Mapped["EngineeringProblem"] = relationship(back_populates="recommendations")
