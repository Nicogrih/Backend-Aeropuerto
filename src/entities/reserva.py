import uuid
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Reserva(Base):
    __tablename__ = "reserva"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    id_pasajero = Column(UUID(as_uuid=True), ForeignKey("pasajero.id"), nullable=False)
    id_asiento = Column(UUID(as_uuid=True), ForeignKey("asiento.id"), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    estado_pago = Column(String, nullable=False, default="Pendiente")
    tiempo_expiracion = Column(DateTime, nullable=False)

    pasajero = relationship("Pasajero")
    asiento = relationship("Asiento")