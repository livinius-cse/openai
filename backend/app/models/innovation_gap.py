from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class InnovationGap(Base):
    __tablename__ = "innovation_gaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    engineering_problem_id: Mapped[int] = mapped_column(ForeignKey("engineering_problems.id"), index=True)
    gap_title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    opportunity_score: Mapped[int] = mapped_column(Integer, default=0)
    market_signal: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    problem: Mapped["EngineeringProblem"] = relationship(back_populates="innovation_gaps")
