from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


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

    phase_current_1: list[float] = Field(min_length=4096)
    phase_current_2: list[float] = Field(min_length=4096)
    vibration_1: list[float] = Field(min_length=4096)

    @model_validator(mode="after")
    def validate_sensor_lengths(self):
        lengths = {
            len(self.phase_current_1),
            len(self.phase_current_2),
            len(self.vibration_1),
        }

        if len(lengths) != 1:
            raise ValueError(
                "All sensor data must have the same length."
            )

        return self


class PredictionResponse(PredictionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)