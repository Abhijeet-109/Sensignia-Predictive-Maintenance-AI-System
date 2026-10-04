from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.machine import MachineCreate, MachineResponse
from app.services.machine_service import (
    create_machine,
    get_machine,
    get_machines,
    update_machine,
)


router = APIRouter(
    prefix="/machines",
    tags=["Machines"],
)


@router.post("/", response_model=MachineResponse)
def create(
    data: MachineCreate,
    db: Session = Depends(get_db),
):
    return create_machine(db, data)


@router.get("/", response_model=list[MachineResponse])
def list_all(db: Session = Depends(get_db)):
    return get_machines(db)


@router.get("/{machine_id}", response_model=MachineResponse)
def get_one(
    machine_id: int,
    db: Session = Depends(get_db),
):
    machine = get_machine(db, machine_id)

    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )

    return machine


@router.put("/{machine_id}", response_model=MachineResponse)
def update(
    machine_id: int,
    data: MachineCreate,
    db: Session = Depends(get_db),
):
    machine = update_machine(db, machine_id, data)

    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found",
        )

    return machine