import logging

from fastapi import FastAPI, Depends
from app.core.logging import setup_logging
from app.database.connection import get_db
from sqlalchemy import text

from app.api.v1.router import router as v1_router



setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI (
    title = "Sensignia API",
    description = "Industrial bearing condition monitoring and predictive maintenance backend.",
    version = "1.0.0"
)

@app.get("/health")
def health_check():
    logger.info("Health endpoint was called")
    return {
        "status" : "healthy",
        "service" : "sensignia-api"
    }


@app.get("/db-test")
def database_test(db = Depends (get_db)):
    result = db.execute(text("Select 1"))

    return {
        "database" : "connected",
        "result" : result.scalar()
    }


app.include_router(
    v1_router,
    prefix = "/api/v1"
)
