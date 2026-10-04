from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.security import (
    create_access_token,
    decode_access_token,
    verify_password,
)
from app.database.connection import get_db
from app.models.login_session import LoginSession
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.services.session_service import (
    close_login_session,
    create_login_session,
)

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )

    if not user or not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    login_time = datetime.utcnow()

    user.last_login_at = login_time

    login_session = create_login_session(
        db=db,
        user_id=user.id,
    )

    token = create_access_token(
        user_id=user.id,
        username=user.username,
        role=user.role,
        session_id=login_session.id,
    )

    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 24 * 60 * 60,
    }


@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    session_id = payload.get("session_id")

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token",
        )

    login_session = (
        db.query(LoginSession)
        .filter(
            LoginSession.id == int(session_id)
        )
        .first()
    )

    if not login_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Login session not found",
        )

    if login_session.logout_at is not None:
        return {
            "message": "Already logged out"
        }

    close_login_session(
        db=db,
        session=login_session,
    )

    return {
        "message": "Logout successful"
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user