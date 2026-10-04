from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PredictionBase(BaseModel):
    component_id: int
    model_id: int
    predicted_class: str
    confidence: float = Field(ge=0.0, le=1.0)


class PredictionCreate(PredictionBase):
    pass


class PredictionRequest(BaseModel):
    component_id: int
    model_id: int
    phase_current_1: list[float]
    phase_current_2: list[float]
    vibration_1: list[float]

    

class PredictionResponse(PredictionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)