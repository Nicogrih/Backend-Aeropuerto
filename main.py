from fastapi import FastAPI
from database import engine, Base
from sqlalchemy import text
from database import SessionLocal
import uuid

#Importar modelos de la carpeta models
from models.aeropuerto import Aeropuerto
from models.vuelo import Vuelo

app = FastAPI()

#Crea las tablas automáticamente al iniciar
Base.metadata.create_all(bind=engine)

#Crea aeropuertos manualmente
@app.post("/seed-aeropuertos")
def seed_aeropuertos():
    db = SessionLocal()

    aeropuerto1 = Aeropuerto(
        id=uuid.uuid4(),
        nombre="El Dorado",
        codigo_iata="BOG",
        pais="Colombia",
        es_internacional=True
    )
    
    aeropuerto2 = Aeropuerto(
        id=uuid.uuid4(),
        nombre="JFK International",
        codigo_iata="JFK",
        pais="USA",
        es_internacional=True
    )

    db.add(aeropuerto1)
    db.add(aeropuerto2)
    db.commit()
    db.close()

    return {"message": "Aeropuertos creados"}


#Crea vuelos manualmente
@app.post("/seed-vuelos")
def seed_vuelos():
    db = SessionLocal()

    #Obtener aeropuertos existentes
    aeropuertos = db.query(Aeropuerto).all()

    if len(aeropuertos) < 2:
        db.close()
        return {"error": "necesitas al menos 2 aeropuertos"}
    
    vuelo1 = Vuelo(
        numero_vuelo="AV001",
        id_origen=aeropuertos[0].id,
        id_destino=aeropuertos[1].id,
        tipo="Internacional",
        estado="Programado"
    )

    vuelo2 = Vuelo(
        numero_vuelo="AV002",
        id_origen=aeropuertos[1].id,
        id_destino=aeropuertos[0].id,
        tipo="Internacional",
        estado="Programado"
    )

    db.add(vuelo1)
    db.add(vuelo2)
    db.commit()
    db.close()

    return {"message": "Vuelos creados"}


#Muestra los itinerarios existentes
@app.get("/itinerarios")
def listar_itinerarios():
    db = SessionLocal()

    vuelos = db.query(Vuelo).all()

    resultado = []

    for vuelo in vuelos:
        resultado.append({
            "id_vuelo": str(vuelo.id),
            "numero_vuelo": vuelo.numero_vuelo,
            "origen": {
                "id_aeropuerto": str(vuelo.origen.id),
                "nombre": vuelo.origen.nombre
                },
            "destino": {
                "id_aeropuerto": str(vuelo.destino.id),
                "nombre": vuelo.destino.nombre
                },
            "tipo": vuelo.tipo,
            "estado": vuelo.estado
        })

    db.close()
    return resultado


#Borra vuelos
@app.delete("/vuelos/{vuelo_id}")
def eliminar_vuelo(vuelo_id: str):
    db = SessionLocal()

    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()

    if not vuelo:
        db.close()
        return {"error": "Vuelo no encontrado"}

    db.delete(vuelo)
    db.commit()
    db.close()

    return {"message": "Vuelo eliminado correctamente"}

#Borra aeropuertos
@app.delete("/aeropuertos/{aeropuerto_id}")
def eliminar_aeropuerto(aeropuerto_id: str):
    db = SessionLocal()

    aeropuerto = db.query(Aeropuerto).filter(Aeropuerto.id == aeropuerto_id).first()

    if not aeropuerto:
        db.close()
        return {"error": "Aeropuerto no encontrado"}
    
    #Verificar si tiene vuelos asociados
    vuelos_asociados = db.query(Vuelo).filter(
        (Vuelo.id_origen == aeropuerto_id) |
        (Vuelo.id_destino == aeropuerto_id)
    ).first()

    if vuelos_asociados:
        db.close()
        return {"error": "No se puede eliminar el aeropuerto porque tiene vuelos asociados"}
    
    db.delete(aeropuerto)
    db.commit()
    db.close()

    return {"message": "Aeropuerto eliminado correctamente"}


@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"db_response": result.scalar()}



"""@app.get("/")
def read_root():
    return {"Hello": "World"}"""
