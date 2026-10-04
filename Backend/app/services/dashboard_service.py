from sqlalchemy.orm import Session

from app.models.machine import Machine
from app.models.component import Component
from app.models.health import Health
from app.models.prediction import Prediction


def get_machine_dashboard(
    db: Session,
    machine_id: int
):
    machine = (
        db.query(Machine)
        .filter(Machine.id == machine_id)
        .first()
    )

    if not machine:
        return None

    components = (
        db.query(Component)
        .filter(Component.machine_id == machine_id)
        .all()
    )

    machine_health = None

    health_records = (
        db.query(Health)
        .join(Component)
        .filter(Component.machine_id == machine_id)
        .all()
    )

    if health_records:
        average_health = (
            sum(h.health_score for h in health_records)
            / len(health_records)
        )

        worst_health = min(
            health_records,
            key=lambda h: h.health_score
        )

        machine_health = {
            "machine_id": machine_id,
            "health_score": average_health,
            "condition": worst_health.condition,
        }

    component_data = []

    for component in components:
        health = (
            db.query(Health)
            .filter(Health.component_id == component.id)
            .first()
        )

        prediction = (
            db.query(Prediction)
            .filter(
                Prediction.component_id == component.id
            )
            .order_by(
                Prediction.created_at.desc()
            )
            .first()
        )

        component_data.append({
            "id": component.id,
            "name": component.name,
            "component_type": component.component_type,
            "health": health,
            "latest_prediction": prediction,
        })

    return {
        "machine": machine,
        "machine_health": machine_health,
        "components": component_data,
    }