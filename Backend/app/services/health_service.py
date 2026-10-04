from sqlalchemy.orm import Session

from app.models.health import Health


def calculate_health_score(predicted_class: str, confidence: float):
    if predicted_class == "Healthy":
        return confidence * 100

    return (1 - confidence) * 100


def create_or_update_health(
    db: Session,
    component_id: int,
    predicted_class: str,
    confidence: float,
):
    health = (
        db.query(Health)
        .filter(Health.component_id == component_id)
        .first()
    )

    health_score = calculate_health_score(
        predicted_class,
        confidence
    )

    if health:
        health.condition = predicted_class
        health.health_score = health_score
    else:
        health = Health(
            component_id=component_id,
            condition=predicted_class,
            health_score=health_score,
        )
        db.add(health)

    db.commit()
    db.refresh(health)

    return health


def get_component_health(db: Session, component_id: int):
    return (
        db.query(Health)
        .filter(Health.component_id == component_id)
        .first()
    )