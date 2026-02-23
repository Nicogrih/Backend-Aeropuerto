from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime


# ==============================
#  Schema Base
# ==============================

class UsuarioBase(BaseModel):
    nombre: str
    nombre_usuario: str
    email: EmailStr
    telefono: Optional[str] = None


# ==============================
# Schema para Crear Usuario
# ==============================

class UsuarioCreate(UsuarioBase):
    password: str


# ==============================
# Schema para Actualizar Usuario
# ==============================

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    password: Optional[str] = None
    activo: Optional[bool] = None
    es_admin: Optional[bool] = None


# ==============================
# Schema de Respuesta
# ==============================

class UsuarioResponse(UsuarioBase):
    id: UUID
    activo: bool
    es_admin: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime]

    class Config:
        from_attributes = True
