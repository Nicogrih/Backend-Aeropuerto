import uuid
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    id_pasajero = Column(
        UUID(as_uuid=True),
        ForeignKey("pasajeros.id"),
        nullable=False
    )

    id_asiento = Column(
        UUID(as_uuid=True),
        ForeignKey("asientos.id"),
        nullable=False
    )

    fecha_creacion = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    estado_pago = Column(
        String,
        nullable=False,
        default="Pendiente"
    )

    tiempo_expiracion = Column(
        DateTime,
        nullable=False
    )

    # Relaciones
    pasajero = relationship(
        "Pasajero",
        back_populates="reservas"
    )

    asiento = relationship(
        "Asiento",
        back_populates="reservas"
    )