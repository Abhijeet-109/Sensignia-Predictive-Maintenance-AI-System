from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.login_session import LoginSession


def create_login_session(
    db: Session,
    user_id: int
):
    login_time = datetime.utcnow()

    session = LoginSession(
        user_id=user_id,
        login_at=login_time,
        expires_at=(
            login_time
            + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        ),
        duration_seconds=0,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def close_login_session(
    db: Session,
    session: LoginSession
):
    logout_time = datetime.utcnow()

    session.logout_at = logout_time

    end_time = min(
        logout_time,
        session.expires_at
    )

    duration = (
        end_time - session.login_at
    ).total_seconds()

    session.duration_seconds = int(
        max(duration, 0)
    )

    db.commit()
    db.refresh(session)

    return session