from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.sensor import SensorCreate, SensorResponse
from app.services import sensor_service


router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)


@router.post("/", response_model=SensorResponse)
def create_sensor(
    data: SensorCreate,
    db: Session = Depends(get_db)
):
    return sensor_service.create_sensor(db, data)


@router.get("/", response_model=list[SensorResponse])
def get_sensors(
    db: Session = Depends(get_db)
):
    return sensor_service.get_sensors(db)


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db)
):
    sensor = sensor_service.get_sensor(db, sensor_id)

    if not sensor:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return sensor


@router.put("/{sensor_id}", response_model=SensorResponse)
def update_sensor(
    sensor_id: int,
    data: SensorCreate,
    db: Session = Depends(get_db)
):
    sensor = sensor_service.update_sensor(
        db,
        sensor_id,
        data
    )

    if not sensor:
        raise HTTPException(
            status_code=404,
            detail="Sensor not found"
        )

    return sensor