from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum

from src.database.config import Base

class TipoVuelo(str, enum.Enum):
    Nacional = "Nacional"
    Internacional = "Internacional"

class EstadoVuelo(str, enum.Enum):
    Programado = "Programado"
    EnVuelo = "En Vuelo"
    Aterrizado = "Aterrizado"
    Cancelado = "Cancelado"

class Vuelo(Base):
    __tablename__= "vuelos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_vuelo = Column(String, nullable =False)

    id_origen = Column(UUID(as_uuid=True), ForeignKey("aeropuerto.id"), nullable=False)
    id_destino = Column(UUID(as_uuid=True), ForeignKey("aeropuerto.id"), nullable=False)

    tipo = Column(Enum(TipoVuelo), nullable=False)
    estado = Column(Enum(EstadoVuelo), default=EstadoVuelo.Programado, nullable=False)

    origen = relationship(
    "Aeropuerto",
    foreign_keys=[id_origen],
    back_populates="origen_vuelos"
    )

    destino = relationship(
        "Aeropuerto",
        foreign_keys=[id_destino],
        back_populates="destino_vuelos"
    )