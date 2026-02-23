from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.database.config import Base


class Aeropuerto(Base):
    __tablename__ = "aeropuerto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    codigo_iata = Column(String(3), unique=True, nullable=False)
    pais = Column(String, nullable=False)
    es_internacional = Column(Boolean, nullable=False)

    # Relaciones con vuelos
    origen_vuelos = relationship(
        "Vuelo",
        foreign_keys="Vuelo.id_origen",
        back_populates="origen"
    )

    destino_vuelos = relationship(
        "Vuelo",
        foreign_keys="Vuelo.id_destino",
        back_populates="destino"
    )