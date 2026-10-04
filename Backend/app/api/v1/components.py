from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.component import ComponentCreate, ComponentResponse
from app.services import component_service


router = APIRouter(
    prefix="/components",
    tags=["Components"]
)


@router.post("/", response_model=ComponentResponse)
def create_component(
    data: ComponentCreate,
    db: Session = Depends(get_db)
):
    return component_service.create_component(db, data)


@router.get("/", response_model=list[ComponentResponse])
def get_components(
    db: Session = Depends(get_db)
):
    return component_service.get_components(db)


@router.get("/{component_id}", response_model=ComponentResponse)
def get_component(
    component_id: int,
    db: Session = Depends(get_db)
):
    component = component_service.get_component(db, component_id)

    if not component:
        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    return component


@router.put("/{component_id}", response_model=ComponentResponse)
def update_component(
    component_id: int,
    data: ComponentCreate,
    db: Session = Depends(get_db)
):
    component = component_service.update_component(
        db,
        component_id,
        data
    )

    if not component:
        raise HTTPException(
            status_code=404,
            detail="Component not found"
        )

    return component