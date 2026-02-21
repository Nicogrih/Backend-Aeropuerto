from fastapi import FastAPI
import uvicorn
from src.database.config import engine, Base
from sqlalchemy import text
from src.database.config import SessionLocal
import uuid

#Importar modelos de la carpeta models
from src.entities.aeropuerto import Aeropuerto
from src.entities.vuelo import Vuelo
from src.entities.pasajero import Pasajero
from src.entities.tarifa_clase import TarifaClase
from src.entities.asiento import Asiento
from src.entities.reserva import Reserva

#Verificar el estado de la reserva
from datetime import datetime, timedelta

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host= "0.0.0.0", port=8000)



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

""""
#crear pasajeros manualmente
@app.post("/pasajeros")
def crear_pasajeros(
    nombre_completo: str,
    email: str,
    nacionalidad: str,
    documento_pasaporte: str | None = None,
    documento_visa: str | None = None
):
    db = SessionLocal()

    pasajero = Pasajero(
        nombre_completo=nombre_completo,
        email=email,
        nacionalidad=nacionalidad,
        documento_pasaporte=documento_pasaporte,
        documento_visa=documento_visa
    )

    db.add(pasajero)
    db.commit()
    db.refresh(pasajero)
    db.close()

    return {"message": "Pasajero creado","id": str(pasajero.id)}

#listar pasajeros
@app.get("/pasajeros")
def listar_pasajeros():
    db = SessionLocal()

    pasajeros = db.query(Pasajero).all()
    resultado = []
    for p in pasajeros:
        resultado.append({
            "id": str(p.id),
            "nombre": p.nombre_completo,
            "email": p.email,
            "nacionalidad": p.nacionalidad
        })

    db.close()
    return resultado

#borrar pasajero
@app.delete("/pasajeros/{pasajero_id}")
def eliminar_pasajero(pasajero_id : str):
    db = SessionLocal()

    pasajero = db.query(Pasajero).filter(Pasajero.id == pasajero_id).first()
    if not pasajero:
        db.close()
        return {"error": "Pasajero no encontrado"}

    db.delete(pasajero)
    db.commit()
    db.close()

    return {"message": "Pasajero eliminado"}

#crear tarifa manualmente
@app.post("/tarifas")
def crear_tarifa(
    nombre_clase: str,
    precio_base: float,
    flexibilidad: bool = False,
    prioridad_embarque: bool = False
):
    db = SessionLocal()

    tarifa = TarifaClase(
        nombre_clase=nombre_clase,
        precio_base=precio_base,
        flexibilidad=flexibilidad,
        prioridad_embarque=prioridad_embarque
    )

    db.add(tarifa)
    db.commit()
    db.refresh(tarifa)
    db.close()

    return {
        "message": "Tarifa creada","id": str(tarifa.id)
    }

#listar tarifas
@app.get("/tarifas")
def listar_tarifas():
    db = SessionLocal()

    tarifas = db.query(TarifaClase).all()

    resultado = []
    for t in tarifas:
        resultado.append({
            "id": str(t.id),
            "nombre_clase": t.nombre_clase,
            "precio_base": float(t.precio_base),
            "flexibilidad": t.flexibilidad,
            "prioridad_embarque": t.prioridad_embarque
        })

    db.close()
    return resultado

#borrar tarifa
@app.delete("/tarifa/{tarifa_id}")
def eliminar_tarifa(tarifa_id: str):
    db = SessionLocal()

    tarifa = db.query(TarifaClase).filter(TarifaClase.id == tarifa_id).first()

    if not tarifa:
        db.close()
        return {"error": "Tarifa no encontrada"}

    db.delete(tarifa)
    db.commit()
    db.close()

    return {"message": "Tarifa eliminada"}


#crear asiento manualmente
@app.post("/asientos")
def crer_asientos(
    codigo_fisico: str,
    id_vuelo: str,
    id_tarifa: str
):
    db = SessionLocal()

    vuelo = db.query(Vuelo).filter(Vuelo.id == id_vuelo).first()
    if not vuelo:
        db.close()
        return {"error": "Vuelo no existe"}

    tarifa = db.query(TarifaClase).filter(TarifaClase.id == id_tarifa).first()
    if not tarifa:
        db.close()
        return {"error": "Tarifa no existe"}

    asiento = Asiento(
        codigo_fisico=codigo_fisico,
        id_vuelo=id_vuelo,
        id_tarifa=id_tarifa,
        estado_actual="Disponible"
    )

    db.add(asiento)
    db.commit()
    db.refresh(asiento)
    db.close()

    return {
        "message": "Asiento creado","id": str(asiento.id)
    }

#listar asientos
@app.get("/asientos")
def listar_asientos():
    db = SessionLocal()

    asientos = db.query(Asiento).all()

    resultado = []
    for a in asientos:
        resultado.append({
            "id": str(a.id),
            "codigo": a.codigo_fisico,
            "vuelo": str(a.id_vuelo),
            "tarifa": str(a.id_tarifa),
            "estado": a.estado_actual
        })

    db.close()
    return resultado

#borrar asiento
@app.delete("/asientos/{asiento_id}")
def eliminar_asiento(asiento_id: str):
    db = SessionLocal()

    asiento = db.query(Asiento).filter(Asiento.id == asiento_id).first()

    if not asiento:
        db.close()
        return {"error": "Asiento no encontrado"}

    db.delete(asiento)
    db.commit()
    db.close()

    return {"message": "Asiento eliminado"}

#crear reserva manualmente
@app.post("/reservas")
def crear_reserva(
    id_pasajero: str,
    id_asiento: str,
    minutos_expiracion: int = 30
):
    db = SessionLocal()

    # validar pasajero
    pasajero = db.query(Pasajero).filter(Pasajero.id == id_pasajero).first()
    if not pasajero:
        db.close()
        return {"error": "Pasajero no existe"}

    # validar asiento
    asiento = db.query(Asiento).filter(Asiento.id == id_asiento).first()
    if not asiento:
        db.close()
        return {"error": "Asiento no existe"}

    # validar disponibilidad
    if asiento.estado_actual != "Disponible":
        db.close()
        return {"error": "Asiento no disponible"}

    # calcular expiración
    expiracion = datetime.utcnow() + timedelta(minutes=minutos_expiracion)

    # crear reserva
    reserva = Reserva(
        id_pasajero=id_pasajero,
        id_asiento=id_asiento,
        tiempo_expiracion=expiracion,
        estado_pago="Pendiente"
    )

    db.add(reserva)

    #marcar asiento como reservado
    asiento.estado_actual = "Reservado"

    db.commit()
    db.refresh(reserva)
    db.close()

    return {
        "message": "Reserva creada",
        "id_reserva": str(reserva.id),
        "expira_en": expiracion
    }

#listar reserva
@app.get("/reservas")
def listar_reservas():
    db = SessionLocal()

    reservas = db.query(Reserva).all()

    resultado = []
    for r in reservas:
        resultado.append({
            "id": str(r.id),
            "pasajero": r.pasajero.nombre_completo if r.pasajero else None,
            "asiento": r.asiento.codigo_fisico if r.asiento else None,
            "estado_pago": r.estado_pago,
            "expira": r.tiempo_expiracion
        })

    db.close()
    return resultado

#pagar reserva
@app.put("/reservas/{reserva_id}/pagar")
def pagar_reserva(reserva_id: str):
    db = SessionLocal()

    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        db.close()
        return {"error": "Reserva no encontrada"}

    reserva.estado_pago = "Pagado"
    reserva.asiento.estado_actual = "Ocupado"

    db.commit()
    db.close()

    return {"message": "Reserva pagada"}

#eliminar reserva
@app.delete("/reservas/{reserva_id}")
def cancelar_reserva(reserva_id: str):
    db = SessionLocal()

    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()

    if not reserva:
        db.close()
        return {"error": "Reserva no encontrada"}

    # liberar asiento
    reserva.asiento.estado_actual = "Disponible"

    db.delete(reserva)
    db.commit()
    db.close()

    return {"message": "Reserva cancelada"}"""

"""@app.get("/")
def read_root():
    return {"Hello": "World"}"""