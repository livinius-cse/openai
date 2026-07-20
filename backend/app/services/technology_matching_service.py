from app.schemas.analysis import EngineeringProblemRead, TechnologyRecommendationRead


class TechnologyMatchingService:
    """Matches solutions to problems. Mock implementation for Phase 2."""

    def match(self, problem: EngineeringProblemRead) -> list[TechnologyRecommendationRead]:
        return [
            TechnologyRecommendationRead(id=201, engineering_problem_id=problem.id, technology_name="Grid-edge battery orchestration", rationale="Balances peak demand and supports distributed storage during heat events.", maturity_level="Commercial", match_score=91),
            TechnologyRecommendationRead(id=202, engineering_problem_id=problem.id, technology_name="AI-assisted demand response", rationale="Reduces non-critical demand when grid capacity is constrained.", maturity_level="Scaling", match_score=84),
        ]
