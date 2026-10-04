from fastapi import APIRouter

from app.api.v1.machines import router as machines_router
from app.api.v1.components import router as components_router
from app.api.v1.sensors import router as sensors_router


router = APIRouter()

router.include_router(machines_router)
router.include_router(components_router)
router.include_router(sensors_router)