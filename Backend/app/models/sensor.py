
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(primary_key=True)

    component_id: Mapped[int] = mapped_column(
        ForeignKey("components.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    sensor_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    unit: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )