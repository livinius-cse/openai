from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class AnalysisRequest(BaseModel):
    title: str = Field(min_length=3, max_length=500, examples=["Heatwave pressures city power grids"])
    content: str = Field(min_length=20, examples=["A sustained heatwave is increasing electricity demand across urban districts."])
    source_url: HttpUrl = Field(examples=["https://example.com/news/heatwave-grid"])
    source_name: str | None = Field(default=None, max_length=255, examples=["Example News"])
    published_at: datetime | None = None


class EngineeringProblemRead(BaseModel):
    id: int
    title: str
    summary: str
    sector: str
    region: str | None
    severity: str
    urgency_score: int = Field(ge=0, le=100)


class TechnologyRecommendationRead(BaseModel):
    id: int
    engineering_problem_id: int
    technology_name: str
    rationale: str
    maturity_level: str
    match_score: int = Field(ge=0, le=100)


class InnovationGapRead(BaseModel):
    id: int
    engineering_problem_id: int
    gap_title: str
    description: str
    opportunity_score: int = Field(ge=0, le=100)
    market_signal: str


class AnalysisResponse(BaseModel):
    article_id: int
    status: str
    problem: EngineeringProblemRead
    recommendations: list[TechnologyRecommendationRead]
    innovation_gap: InnovationGapRead
