from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    id: int
    component_id: int
    condition: str
    health_score: float = Field(ge=0.0, le=100.0)
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)