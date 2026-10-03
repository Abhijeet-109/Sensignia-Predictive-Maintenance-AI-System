import logging
from fastapi import FastAPI
from app.core.logging import setup_logging

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

