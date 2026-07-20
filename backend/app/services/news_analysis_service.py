from app.schemas.analysis import AnalysisRequest, AnalysisResponse, EngineeringProblemRead, TechnologyRecommendationRead
from app.services.innovation_gap_service import InnovationGapService
from app.services.problem_extraction_service import ProblemExtractionService
from app.services.technology_matching_service import TechnologyMatchingService


class NewsAnalysisService:
    """Coordinates the Phase 2 analysis pipeline using deterministic mock services."""

    def __init__(self) -> None:
        self.problem_extraction = ProblemExtractionService()
        self.technology_matching = TechnologyMatchingService()
        self.innovation_gap = InnovationGapService()

    def analyze(self, article: AnalysisRequest) -> AnalysisResponse:
        problem = self.problem_extraction.extract(article.title, article.content)
        recommendations = self.technology_matching.match(problem)
        gap = self.innovation_gap.identify(problem)
        return AnalysisResponse(article_id=1, status="mock_analysis_complete", problem=problem, recommendations=recommendations, innovation_gap=gap)

    def list_problems(self) -> list[EngineeringProblemRead]:
        return [self.problem_extraction.extract("Heatwave pressures city power grids", "Mock content")]

    def list_recommendations(self) -> list[TechnologyRecommendationRead]:
        return self.technology_matching.match(self.list_problems()[0])
