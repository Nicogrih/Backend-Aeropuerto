# Modelo de Datos

## Entidades y atributos

### Aeropuerto
- `id`: UUID (PK)
- `nombre`: VARCHAR
- `codigo_iata`: CHAR(3)
- `pais`: VARCHAR
- `es_internacional`: BOOLEAN

### Vuelo
- `id`: UUID (PK)
- `numero_vuelo`: VARCHAR
- `id_origen`: UUID (FK → Aeropuerto)
- `id_destino`: UUID (FK → Aeropuerto)
- `tipo`: ENUM (Nacional, Internacional)
- `estado`: ENUM (Programado, En Vuelo, Aterrizado, Cancelado)

### Pasajero
- `id`: UUID (PK)
- `nombre_completo`: VARCHAR
- `email`: VARCHAR (UNIQUE)
- `nacionalidad`: VARCHAR
- `documento_pasaporte`: VARCHAR (con validación regex)
- `documento_visa`: VARCHAR (con validación regex)

### Tarifa_Clase
- `id`: UUID (PK)
- `nombre_clase`: VARCHAR
- `precio_base`: DECIMAL
- `flexibilidad`: BOOLEAN
- `prioridad_embarque`: BOOLEAN

### Asiento
- `id`: UUID (PK)
- `codigo_fisico`: VARCHAR
- `id_vuelo`: UUID (FK → Vuelo)
- `id_tarifa`: UUID (FK → Tarifa_Clase)
- `estado_actual`: ENUM (Disponible, Reservado, Ocupado)

### Reserva
- `id`: UUID (PK)
- `id_pasajero`: UUID (FK → Pasajero)
- `id_asiento`: UUID (FK → Asiento)
- `fecha_creacion`: TIMESTAMP
- `estado_pago`: ENUM (Pendiente, Completado, Fallido)
- `tiempo_expiracion`: TIMESTAMP → calculado como `fecha_creacion + 60 minutos`

## Relaciones principales

- **Aeropuerto** se relaciona con **Vuelo** en dos roles:
  - Un aeropuerto puede ser origen de muchos vuelos (1:N).
  - Un aeropuerto puede ser destino de muchos vuelos (1:N).
  - *Nota:* En el modelo, `Vuelo` tiene dos claves foráneas a `Aeropuerto`.

- **Vuelo** se relaciona con **Asiento** en **1:N**.
  - Un vuelo tiene muchos asientos; cada asiento pertenece a un único vuelo.

- **Tarifa_Clase** se relaciona con **Asiento** en **1:N**.
  - Una tarifa puede aplicarse a muchos asientos; cada asiento tiene una única tarifa.

- **Pasajero** se relaciona con **Reserva** en **1:N**.
  - Un pasajero puede hacer muchas reservas (en diferentes momentos/vuelos); cada reserva pertenece a un solo pasajero.

- **Asiento** se relaciona con **Reserva** en **1:N**.
  - Un asiento puede estar involucrado en varias reservas a lo largo del tiempo (histórico), pero solo una reserva activa por vez (controlado por `estado_actual` del asiento y la lógica de negocio). La relación actual se modela como 1:N desde asiento hacia reserva.

## Reglas de integridad destacadas

- El campo `email` en `pasajero` es **único**.
- Los documentos `pasaporte` y `visa` tienen restricciones `CHECK` con expresiones regulares, permitiendo valores nulos (útil para pasajeros de vuelos nacionales sin visa).
- El índice `idx_reserva_expiracion` filtra solo reservas pendientes para optimizar el proceso de limpieza automática.