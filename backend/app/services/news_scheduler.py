import logging
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.news_ingestion_service import NewsIngestionService

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler(timezone="UTC")


def ingest_with_retry() -> None:
    """Retry a failed full ingestion run up to three times with logs."""
    for attempt in range(1, 4):
        db = SessionLocal()
        try:
            results = NewsIngestionService(db).ingest_all()
            failed = [result for result in results if result.message]
            if not failed:
                logger.info("News ingestion completed: %s", results)
                return
            raise RuntimeError(f"{len(failed)} provider jobs failed")
        except Exception:
            logger.exception("News ingestion attempt %s/3 failed", attempt)
            if attempt == 3:
                return
            sleep(attempt * 2)
        finally:
            db.close()


def start_news_scheduler() -> None:
    if scheduler.running:
        return
    interval = get_settings().news_ingestion_interval_minutes
    scheduler.add_job(ingest_with_retry, "interval", minutes=interval, id="news-ingestion", replace_existing=True, max_instances=1, coalesce=True)
    scheduler.start()
    logger.info("News scheduler started: every %s minutes", interval)


def stop_news_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
