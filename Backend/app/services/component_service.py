from sqlalchemy.orm import Session

from app.models.component import Component
from app.schemas.component import ComponentCreate


def create_component(db: Session, data: ComponentCreate):
    component = Component(**data.model_dump())

    db.add(component)
    db.commit()
    db.refresh(component)

    return component


def get_component(db: Session, component_id: int):
    return db.query(Component).filter(Component.id == component_id).first()


def get_components(db: Session):
    return db.query(Component).all()


def update_component(
    db: Session,
    component_id: int,
    data: ComponentCreate
):
    component = get_component(db, component_id)

    if not component:
        return None

    for field, value in data.model_dump().items():
        setattr(component, field, value)

    db.commit()
    db.refresh(component)

    return component