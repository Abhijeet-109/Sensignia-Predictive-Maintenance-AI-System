from sqlalchemy.orm import Session

from app.models.machine import Machine
from app.schemas.machine import MachineCreate


def create_machine(db: Session, data: MachineCreate):
    machine = Machine(**data.model_dump())

    db.add(machine)
    db.commit()
    db.refresh(machine)

    return machine


def get_machine(db: Session, machine_id: int):
    return db.query(Machine).filter(Machine.id == machine_id).first()


def get_machines(db: Session):
    return db.query(Machine).all()


def update_machine(db: Session, machine_id: int, data: MachineCreate):
    machine = get_machine(db, machine_id)

    if not machine:
        return None

    for field, value in data.model_dump().items():
        setattr(machine, field, value)

    db.commit()
    db.refresh(machine)

    return machine