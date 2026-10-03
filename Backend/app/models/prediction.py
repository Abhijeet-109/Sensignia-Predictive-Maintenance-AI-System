
from datetime import datetime

from sqlalchemy import ForeignKey, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)

    component_id: Mapped[int] = mapped_column(
        ForeignKey("components.id"),
        nullable=False
    )

    model_id: Mapped[int] = mapped_column(
        ForeignKey("models.id"),
        nullable=False
    )

    predicted_class: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )