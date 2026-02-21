import uuid
from sqlalchemy import CheckConstraint, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base

class Pasajero():
    __tablename__ = "pasajero"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_completo = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    nacionalidad = Column(String, nullable=False)
    documento_pasaporte = Column(String, nullable=True)
    documento_visa = Column(String, nullable=True)

    reservas = relationship("Reserva", back_populates="pasajero")
    
    __table_args__ = (
        CheckConstraint(
            "documento_pasaporte IS NULL OR documento_pasaporte ~ '^[A-Z]{1,2}[0-9]{6,8}$'",
            name="pasaporte_formato"
        ),
        CheckConstraint(
            "documento_visa IS NULL OR documento_visa ~ '^[0-9]{8}$'",
            name="visa_formato"
        ),
    )