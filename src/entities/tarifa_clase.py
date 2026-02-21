import uuid
from sqlalchemy import Column, String, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class TarifaClase(Base):
    __tablename__ = "tarifa_clase"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_clase = Column(String, nullable=False)
    precio_base = Column(Numeric(10,2), nullable=False)
    flexibilidad = Column(Boolean, nullable=False, default=False)
    prioridad_embarque = Column(Boolean, nullable=False, default=False)
