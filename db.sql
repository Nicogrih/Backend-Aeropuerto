-- 1. CREAR BASE DE DATOS
CREATE DATABASE vuelos_db;

-- 2. HABILITAR EXTENSIÓN PARA UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 3. CREAR TIPOS ENUM
CREATE TYPE tipo_vuelo AS ENUM ('Nacional', 'Internacional');
CREATE TYPE estado_vuelo AS ENUM ('Programado', 'En Vuelo', 'Aterrizado', 'Cancelado');
CREATE TYPE estado_asiento AS ENUM ('Disponible', 'Reservado', 'Ocupado');
CREATE TYPE estado_pago AS ENUM ('Pendiente', 'Completado', 'Fallido');

-- 4. TABLA AEROPUERTO
CREATE TABLE aeropuerto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre VARCHAR NOT NULL,
    codigo_iata CHAR(3) NOT NULL,
    pais VARCHAR NOT NULL,
    es_internacional BOOLEAN NOT NULL DEFAULT false
);

-- 5. TABLA VUELO
CREATE TABLE vuelo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    numero_vuelo VARCHAR NOT NULL,
    id_origen UUID NOT NULL,
    id_destino UUID NOT NULL,
    tipo tipo_vuelo NOT NULL,
    estado estado_vuelo NOT NULL DEFAULT 'Programado',
    CONSTRAINT fk_vuelo_origen FOREIGN KEY (id_origen) REFERENCES aeropuerto(id),
    CONSTRAINT fk_vuelo_destino FOREIGN KEY (id_destino) REFERENCES aeropuerto(id)
);

-- 6. TABLA PASAJERO
CREATE TABLE pasajero (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre_completo VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    nacionalidad VARCHAR NOT NULL,
    documento_pasaporte VARCHAR,
    documento_visa VARCHAR,
    CONSTRAINT pasaporte_formato CHECK (
        documento_pasaporte IS NULL OR documento_pasaporte ~ '^[A-Z]{1,2}[0-9]{6,8}$'
    ),
    CONSTRAINT visa_formato CHECK (
        documento_visa IS NULL OR documento_visa ~ '^[0-9]{8}$'
    )
);

-- 7. TABLA TARIFA_CLASE
CREATE TABLE tarifa_clase (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre_clase VARCHAR NOT NULL,
    precio_base DECIMAL(10,2) NOT NULL,
    flexibilidad BOOLEAN NOT NULL DEFAULT false,
    prioridad_embarque BOOLEAN NOT NULL DEFAULT false
);

-- 8. TABLA ASIENTO
CREATE TABLE asiento (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_fisico VARCHAR NOT NULL,
    id_vuelo UUID NOT NULL,
    id_tarifa UUID NOT NULL,
    estado_actual estado_asiento NOT NULL DEFAULT 'Disponible',
    CONSTRAINT fk_asiento_vuelo FOREIGN KEY (id_vuelo) REFERENCES vuelo(id),
    CONSTRAINT fk_asiento_tarifa FOREIGN KEY (id_tarifa) REFERENCES tarifa_clase(id)
);

-- 9. TABLA RESERVA
CREATE TABLE reserva (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    id_pasajero UUID NOT NULL,
    id_asiento UUID NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado_pago estado_pago NOT NULL DEFAULT 'Pendiente',
    tiempo_expiracion TIMESTAMP NOT NULL,
    CONSTRAINT fk_reserva_pasajero FOREIGN KEY (id_pasajero) REFERENCES pasajero(id),
    CONSTRAINT fk_reserva_asiento FOREIGN KEY (id_asiento) REFERENCES asiento(id)
);

-- 10. ÍNDICES PARA RENDIMIENTO
CREATE INDEX idx_vuelo_origen ON vuelo(id_origen);
CREATE INDEX idx_vuelo_destino ON vuelo(id_destino);
CREATE INDEX idx_asiento_vuelo ON asiento(id_vuelo);
CREATE INDEX idx_reserva_pasajero ON reserva(id_pasajero);
CREATE INDEX idx_reserva_asiento ON reserva(id_asiento);
CREATE INDEX idx_reserva_expiracion ON reserva(tiempo_expiracion) WHERE estado_pago = 'Pendiente';