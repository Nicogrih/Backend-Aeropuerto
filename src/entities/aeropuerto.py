import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from database import Base

class Aeropuerto(Base):
    __tablename__ = "aeropuerto"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, nullable=False)
    codigo_iata = Column(String(3), nullable=False)
    pais = Column(String, nullable=False)
    es_internacional = Column(Boolean, nullable=False, default=False)