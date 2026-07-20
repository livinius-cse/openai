from app.schemas.analysis import EngineeringProblemRead, InnovationGapRead


class InnovationGapService:
    """Identifies unmet solution space. Mock implementation for Phase 2."""

    def identify(self, problem: EngineeringProblemRead) -> InnovationGapRead:
        return InnovationGapRead(id=301, engineering_problem_id=problem.id, gap_title="Affordable neighborhood-scale cooling and storage", description="Existing solutions focus on utilities or individual buildings, leaving dense low-income districts underserved.", opportunity_score=82, market_signal="Growing peak-demand and heat-risk signals")
