from fastapi import APIRouter

from app.api.v1.machines import router as machines_router
from app.api.v1.components import router as components_router
from app.api.v1.sensors import router as sensors_router
from app.api.v1.predictions import router as predictions_router
from app.api.v1.health import router as health_router
from app.api.v1.dashboard import router as dashboard_router

router = APIRouter()

router.include_router(machines_router)
router.include_router(components_router)
router.include_router(sensors_router)
router.include_router(predictions_router)
router.include_router(health_router)
router.include_router(dashboard_router)