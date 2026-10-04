from sqlalchemy.orm import Session

from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate


def create_sensor(db: Session, data: SensorCreate):
    sensor = Sensor(**data.model_dump())

    db.add(sensor)
    db.commit()
    db.refresh(sensor)

    return sensor


def get_sensor(db: Session, sensor_id: int):
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def get_sensors(db: Session):
    return db.query(Sensor).all()


def update_sensor(
    db: Session,
    sensor_id: int,
    data: SensorCreate
):
    sensor = get_sensor(db, sensor_id)

    if not sensor:
        return None

    for field, value in data.model_dump().items():
        setattr(sensor, field, value)

    db.commit()
    db.refresh(sensor)

    return sensor