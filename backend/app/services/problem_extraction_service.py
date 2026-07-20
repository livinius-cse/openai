from app.schemas.analysis import EngineeringProblemRead


class ProblemExtractionService:
    """Extracts an engineering problem from an article. Mock implementation for Phase 2."""

    def extract(self, article_title: str, _content: str) -> EngineeringProblemRead:
        return EngineeringProblemRead(
            id=101,
            title="Urban power-grid resilience during extreme heat",
            summary=f"Mock extraction based on: {article_title}",
            sector="Energy infrastructure",
            region="South Asia",
            severity="high",
            urgency_score=86,
        )
