import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Usuario(Base):
    __tablename__ = "tbl_usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    contraseña_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
    es_admin = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # productos = relationship(
    #     "Producto", back_populates="usuario", foreign_keys="Producto.usuario_id"
    # )

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"