from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import get_machine_dashboard


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/machines/{machine_id}",
    response_model=DashboardResponse
)
def get_dashboard(
    machine_id: int,
    db: Session = Depends(get_db)
):
    dashboard = get_machine_dashboard(
        db,
        machine_id
    )

    if not dashboard:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    return dashboard