# Análisis y Diseño - Sistema AeroLogic Web

### 📋 Requisitos Identificados
- **Funcionales:**
  - Gestión de aeropuertos, vuelos, pasajeros, tarifas, asientos y reservas.
  - Reserva de asientos con bloqueo de 60 minutos (TTL).
  - Servicio automático de limpieza de reservas expiradas (pendientes > 60 min).
  - Validación de documentos (pasaporte/visa) mediante regex, obligatoria para vuelos internacionales, tanto en frontend como backend.
  - Cálculo de coste en cambios de asiento (upgrade/downgrade) con reglas de no reembolso.
  - Endpoints: GET /itinerarios, POST /reservar, DELETE /cancelar, PUT /validar-docs.
  - Estados visuales de asiento: disponible (verde), bloqueado (amarillo), ocupado (rojo).

- **No funcionales:**
  - (Implícitos) Consistencia en reservas concurrentes.
  - (Implícitos) Rendimiento adecuado para consultas de itinerarios y disponibilidad.
  - (Implícitos) Seguridad: validación en backend para evitar datos corruptos.
  - (Implícitos) Mantenibilidad: código simple y bien estructurado.

- **Implícitos:**
  - Control de concurrencia en reserva de asientos.
  - Manejo de errores y respuestas claras.
  - Posible necesidad de autenticación (no explícita, pero asumimos que se puede omitir en MVP).
  - Historial de cambios no requerido.
  - Integración con pagos reales no necesaria en primera versión.
  - Documentación de API (OpenAPI).

- **Restricciones:**
  - Tecnologías: Python, FastAPI, PostgreSQL.
  - Modelo de datos fijo con 6 entidades.
  - Reglas de negocio definidas (regex, cálculo upgrade, TTL 60 min).

### 🎯 Enfoque KISS Recomendado
- **Solución núcleo:** API REST con FastAPI, SQLAlchemy (o SQLModel) para models, y PostgreSQL. La lógica de negocio se encapsula en servicios. La limpieza de reservas se implementa mediante un endpoint interno `/internal/cleanup` invocado por un cron externo cada minuto.
- **Omisiones conscientes:**
  - Autenticación y autorización (se añade después).
  - Sistema de pagos real (solo estados Pendiente/Completado/Fallido).
  - Historial de cambios de asiento.
  - Notificaciones por email.
  - Optimizaciones avanzadas de base de datos (índices básicos sí).
- **Simplificaciones clave:**
  - Usar UUID como PK (como se pide).
  - Job de limpieza simple vía cron + endpoint en lugar de background tasks complejas.
  - Validaciones con Pydantic + regex.
  - Transacciones con SQLAlchemy para operaciones críticas (reserva, cancelación, cambio).

### 🧩 Desglose del Problema
1. **Configuración inicial**
   - Entorno Python, FastAPI, SQLAlchemy/SQLModel, psycopg2-binary, Alembic.
   - Conexión a PostgreSQL.

2. **Modelos de base de datos**
   - Definir clases SQLAlchemy para las 6 entidades con sus relaciones.
   - Agregar índices: `Vuelo.id_origen`, `Vuelo.id_destino`, `Reserva.tiempo_expiracion`, `Asiento.id_vuelo`.

3. **Migraciones**
   - Usar Alembic para generar migración inicial.

4. **Esquemas Pydantic**
   - Request/response models para cada endpoint.
   - Validadores regex para pasaporte y visa.

5. **Servicios (lógica de negocio)**
   - `VueloService.listar_itinerarios(origen, destino)`
   - `ReservaService.reservar(pasajero_id, asiento_id)` (con bloqueo de fila)
   - `ReservaService.cancelar(reserva_id)` (verifica flexibilidad)
   - `PasajeroService.validar_docs(pasaporte, visa, vuelo_id)`
   - `AsientoService.cambiar_asiento(reserva_id, nuevo_asiento_id)`

6. **Endpoints**
   - `GET /itinerarios` (query params origen, destino)
   - `POST /reservar` (body con pasajero_id, asiento_id)
   - `DELETE /cancelar/{reserva_id}`
   - `PUT /validar-docs` (body con vuelo_id, pasaporte, visa)
   - `GET /vuelos/{vuelo_id}/asientos` (para obtener estados)

7. **Limpieza automática**
   - Endpoint `POST /internal/cleanup` que ejecuta eliminación de reservas expiradas.
   - Script externo (cron) que llama a este endpoint cada minuto.

8. **Pruebas**
   - Unitarias para servicios.
   - Integración para endpoints (pytest + test client).

### ⚡ Optimizaciones Justificadas
- **Índices en columnas de búsqueda y filtro** (bajo costo, gran mejora).
- **Transacciones con `select_for_update()`** en reserva para evitar condiciones de carrera (simple y eficaz).
- **Uso de Enum nativos de PostgreSQL** (o check constraints vía SQLAlchemy) para campos de estado, mejora integridad.
- **Cache en memoria de tarifas** (solo si hay alta frecuencia de cambios de asiento; se puede implementar con `lru_cache` y tiempo de vida corto). En MVP no necesario.

### 📝 Plantilla para el Cliente

**Preguntas para clarificar requisitos:**
1. ¿Los vuelos tienen fecha/hora? El modelo actual no lo incluye; para itinerarios es esencial. ¿Cómo se manejará?
2. ¿La validación de documentos debe persistir los datos en `Pasajero` o solo validar?
3. ¿Qué significa exactamente la política de cancelación según `flexibilidad` de la tarifa? ¿Se puede cancelar siempre pero con costo?
4. En cambio de asiento, ¿se requiere verificar disponibilidad del nuevo asiento? Asumimos que sí.
5. ¿El endpoint `/reservar` debe crear un pasajero si no existe o recibir solo `pasajero_id`?
6. ¿Se necesita autenticación? ¿Los usuarios son anónimos o tienen cuenta?
7. Volumen esperado de usuarios concurrentes para dimensionar concurrencia.
8. ¿Hay requisitos de logging/auditoría?

**Criterios de aceptación (ejemplos):**
- **Reserva exitosa:** Un asiento disponible pasa a reservado y se crea una reserva con expiración 60 min.
- **Reserva concurrente:** Dos intentos simultáneos sobre el mismo asiento: uno falla con error 409.
- **Limpieza automática:** Una reserva pendiente con más de 60 min es eliminada y el asiento vuelve a disponible.
- **Validación documentos:** Vuelo internacional con pasaporte inválido retorna error 400; vuelo nacional no exige visa.
- **Cambio de asiento:** Upgrade requiere pago de diferencia; downgrade se permite sin reembolso solo si la tarifa original es flexible.

**Validación de solución:** Se desplegará un entorno de pruebas donde el cliente podrá ejecutar casos de prueba predefinidos y verificar el comportamiento según los criterios.