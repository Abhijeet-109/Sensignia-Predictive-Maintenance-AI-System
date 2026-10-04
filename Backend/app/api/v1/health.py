from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.health import HealthResponse
from app.services.health_service import get_component_health


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get(
    "/components/{component_id}",
    response_model=HealthResponse
)
def get_health(
    component_id: int,
    db: Session = Depends(get_db)
):
    health = get_component_health(
        db,
        component_id
    )

    if not health:
        raise HTTPException(
            status_code=404,
            detail="Health information not found"
        )

    return health