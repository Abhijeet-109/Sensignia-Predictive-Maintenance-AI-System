
from datetime import datetime

from sqlalchemy import ForeignKey, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Health(Base):
    __tablename__ = "health"

    id: Mapped[int] = mapped_column(primary_key=True)

    component_id: Mapped[int] = mapped_column(
        ForeignKey("components.id"),
        nullable=False
    )

    condition: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    health_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )