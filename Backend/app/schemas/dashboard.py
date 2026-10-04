from datetime import datetime

from pydantic import BaseModel


class PredictionSummary(BaseModel):
    predicted_class: str
    confidence: float
    created_at: datetime


class HealthSummary(BaseModel):
    condition: str
    health_score: float


class ComponentDashboard(BaseModel):
    id: int
    name: str
    component_type: str
    health: HealthSummary | None = None
    latest_prediction: PredictionSummary | None = None


class MachineSummary(BaseModel):
    id: int
    name: str
    machine_type: str
    serial_number: str | None = None


class MachineHealthSummary(BaseModel):
    machine_id: int
    health_score: float
    condition: str


class DashboardResponse(BaseModel):
    machine: MachineSummary
    machine_health: MachineHealthSummary | None = None
    components: list[ComponentDashboard]