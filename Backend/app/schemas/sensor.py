from pydantic import BaseModel, ConfigDict


class SensorBase(BaseModel):
    component_id: int
    name: str
    sensor_type: str
    unit: str | None = None
    description: str | None = None


class SensorCreate(SensorBase):
    pass


class SensorResponse(SensorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)