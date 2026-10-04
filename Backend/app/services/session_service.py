from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.login_session import LoginSession


def create_login_session(
    db: Session,
    user_id: int
):
    session = LoginSession(
        user_id=user_id,
        login_at=datetime.now(timezone.utc),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def close_login_session(
    db: Session,
    session: LoginSession
):
    logout_time = datetime.now(timezone.utc)

    session.logout_at = logout_time

    duration = (
        logout_time - session.login_at
    ).total_seconds()

    session.duration_seconds = int(
        max(duration, 0)
    )

    db.commit()
    db.refresh(session)

    return session