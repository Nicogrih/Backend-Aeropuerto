from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.database.config import engine, Base, SessionLocal
from src.entities.usuarios_entities import Usuarios
from src.schemas.usuarios_schemas import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate
)
# ==============================
# Crear aplicación
# ==============================

app = FastAPI()

# ==============================
# Crear tablas automáticamente
# ==============================

Base.metadata.create_all(bind=engine)

# ==============================
# Dependencia para la BD
# ==============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==============================
# insertando usuario de prueba en la tabla
# ==============================

@app.post("/crear-test")
def crear_test(db: Session = Depends(get_db)):
    nuevo = Usuarios(
        nombre="Angel",
        nombre_usuario="angel123",
        email="angel@test.com",
        contraseña_hash="123456"
    )

    db.add(nuevo)
    db.commit()

# ==============================
# Crea usuarios manualmente 
# ==============================

@app.post("/usuarios", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):

    existente = db.query(Usuarios).filter(
        (Usuarios.email == usuario.email) |
        (Usuarios.nombre_usuario == usuario.nombre_usuario)
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    nuevo = Usuarios(
        nombre=usuario.nombre,
        nombre_usuario=usuario.nombre_usuario,
        email=usuario.email,
        contraseña_hash=usuario.password,  # luego lo hasheamos
        telefono=usuario.telefono
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo

    return {"mensaje": "Usuario creado"}

# ==============================
# lista todos los usuarios (solo muestra los que estan activos)
# ==============================

@app.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuarios).filter(Usuarios.activo == True).all()

# ==============================
# Obtiene usuarios por id 
# ==============================

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: str, db: Session = Depends(get_db)):

    usuario = db.query(Usuarios).filter(
        Usuarios.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario

# ==============================
# actualiza usuarios por id
# ==============================

@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: str, datos: UsuarioUpdate, db: Session = Depends(get_db)):

    usuario = db.query(Usuarios).filter(
        Usuarios.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in datos.model_dump(exclude_unset=True).items():
        if key == "password":
            setattr(usuario, "contraseña_hash", value)
        else:
            setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    return usuario

# ==============================
# desactiva usuarios por id
# ==============================

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: str, db: Session = Depends(get_db)):

    usuario = db.query(Usuarios).filter(
        Usuarios.id == usuario_id
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.activo = False
    db.commit()

    return {"mensaje": "Usuario desactivado correctamente"}

# ==============================
# Endpoint prueba conexión BD (no hace nada solo es para ver si funciona fastapi)
# ==============================

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"db_response": result.scalar()}

# ==============================
# Ejecutar servidor
# ==============================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)