import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base

class Asiento(Base):
    __tablename__ = "asiento"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_fisico = Column(String, nullable=False)

    id_vuelo = Column(UUID(as_uuid=True), ForeignKey("vuelo.id"), nullable=False)
    id_tarifa = Column(UUID(as_uuid=True), ForeignKey("tarifa_clase.id"), nullable=False)

    estado_actual = Column(String, nullable=False, default="Disponible")

    # relaciones
    vuelo = relationship("Vuelo", back_populates="asientos")
    tarifa = relationship("TarifaClase", back_populates="asientos")
    reservas = relationship("Reserva", back_populates="asiento")