import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.news import router as news_router
from app.api.v1.router import router as v1_router
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
import app.models  # noqa: F401 -- registers database models with SQLAlchemy metadata
from app.services.news_scheduler import start_news_scheduler, stop_news_scheduler

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
    Base.metadata.create_all(bind=engine)
    start_news_scheduler()
    yield
    stop_news_scheduler()


app = FastAPI(
    title="ForgeAI API",
    version="0.3.0",
    description="Live Problem Intelligence Pipeline. Provider ingestion is normalized; GPT analysis is not enabled.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_router, prefix="/api/v1")
app.include_router(news_router)
