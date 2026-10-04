from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class LoginSession(Base):
    __tablename__ = "login_sessions"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    login_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    logout_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    duration_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )