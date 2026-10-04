from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import require_roles
from app.core.security import hash_password
from app.database.connection import get_db
from app.models.user import User
from app.schemas.auth import (
    CreateUserRequest,
    UserResponse,
)


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post(
    "/users",
    response_model=UserResponse
)
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    if data.role not in {"admin", "technician"}:
        raise HTTPException(
            status_code=400,
            detail="Role must be admin or technician"
        )

    existing_user = (
        db.query(User)
        .filter(
            (User.username == data.username)
            | (User.email == data.email)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(
            data.password
        ),
        role=data.role,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    return db.query(User).all()


@router.patch(
    "/users/{user_id}/deactivate"
)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin")
    ),
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot deactivate themselves"
        )

    user.is_active = False

    db.commit()

    return {
        "message": "User deactivated successfully"
    }