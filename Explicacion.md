##  Clases (Modelos de Base de Datos)
Compañeros realice los otros endpoints faltantes, verificarlos para comprobar si estan hechos de manera correcta, cualquier sugerencia o correccion me la hacen saber.
### Pasajero
Campos:
- id → identificador UUID
- nombre_completo → nombre del pasajero
- email → correo único
- nacionalidad → país del pasajero
- documento_pasaporte → opcional con validación de formato
- documento_visa → opcional con validación de formato

Este modelo permite registrar la información personal necesaria para realizar reservas en el sistema.

---

### TarifaClase
Define los tipos de tarifa disponibles.

Campos:
- id → identificador UUID
- nombre_clase → nombre de la tarifa (Ej: Económica, Ejecutiva)
- precio_base → costo base del tiquete
- flexibilidad → indica si permite cambios
- prioridad_embarque → acceso prioritario

---

### Asiento
Representa los asientos disponibles en cada vuelo.

Campos:
- id → identificador UUID
- codigo_fisico → número del asiento (Ej: 12A)
- id_vuelo → vuelo al que pertenece
- id_tarifa → tarifa asignada
- estado_actual → disponible, reservado u ocupado

Relaciones:
- pertenece a un vuelo
- pertenece a una tarifa

---

### Reserva
Representa la reserva de un asiento por un pasajero.

Campos:
- id → identificador UUID
- id_pasajero → pasajero que reserva
- id_asiento → asiento reservado
- fecha_creacion → fecha automática
- estado_pago → pendiente, pagado o cancelado
- tiempo_expiracion → fecha límite de pago

Relaciones:
- pertenece a un pasajero
- pertenece a un asiento

---

# Endpoints Implementados

## Endpoints de carga inicial

# Estado actual

El backend permite:

- crear aeropuertos y vuelos de prueba  
- registrar pasajeros  
- consultar itinerarios  
- manejar relaciones entre tablas  
- eliminar registros con validación 