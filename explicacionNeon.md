Compañeros, he estado probando una pagina que me sirvio el semestre pasado con la materia de programación de software que se llama Neon Console, creo que el profe la menciono en la clase del 14 de febrero para crear una base de datos y es gratis. Les propongo usar esta pagina para hacer este proyecto si les parece bien.

Estos fueron los pasos que realicé para dejar el backend conectado a la base de datos en Neon:

1. Creación del proyecto en Neon:

- Creé un nuevo proyecto en Neon Console.
- Obtuve el connection string que proporciona Neon.
- Ese connection string es el que permite que nuestro Backend en FastAPI se conecte a PostgreSQL en la nube

2. Creacion del archivo .env:

- Hice un archivo .env que se utiliza para guardar variables de entorno
- Allí agrege: DATABASE_URL=postgresql+psycopg2://usuario:password@host/neondb
- Agregé +psycopg2 porque SQLAlchemy lo necesita como driver. Psycopg2 es un adaptador de la base de datos de PostgreSQL que permite ejecutar consultas SQL, manejar transacciones y trabajar con datos de PostgreSQL de manera síncronica
- El .env está ignorado en .gitignore para no subir credenciales al repositorio

3. Configuración de database.py:

- Hice un archivo database.py que:
- Crea el engine de conexión
- Crea SessionLocal para manejar sesiones
- Define Base = declarative_base() para los modelos

Esto permite que cualquier modelo se conecte a la base

4. Creación de modelos en python

Hice las tablas usando SQLAlchemy desde los modelos:
- models/aeropuerto.py
- models/vuelo.py
Ambos heredan de Base

5. Creación automatica de tablas:

En main.py agregué
- Base.metadata.create_all(bind=engine)
Esto hace que, al iniciar el servidor, SQLAlchemy cree automaticamente las tablas en Neon si no existen.

6. Inserté datos de prueba:

Agregé endpoints temporales:
- POST /seed-aeropuertos
- POST /seed-vuelos

para poder agregar vuelos y aeropuertos de prueba y probar el endpoint

7. Endpoint funcional implementado
- GET /itinerarios

Este endpoint:
- Consulta los vuelos
- Usa las relaciones con Aeropuerto

Devuelve:

- ID del vuelo
- ID y nombre del aeropuerto origen
- ID y nombre del aeropuerto destino
- Tipo
- Estado

Actualmente el backend ya:
- Está conectado a Neon
- Tiene tablas creadas automáticamente
- Puede insertar datos
- Puede consultar itinerarios
- Puede eliminar vuelos y aeropuertos con validación

para poder probar la base de datos:

1. Abran la terminal (con CTRL+Ñ)

2. py -m uvicorn main:app --reload (comprobar si funciona fastapi)

3. Les aparecera que Uvicorn esta corriendo en este enlace "http://127.0.0.1:8000" (pueden finalizar con CTRL+C)

4. Despues hagan Ctrl + click encima del enlace y los enviara a una pagina, luego se vuelven a colocar en el enlace "http://127.0.0.1:8000" y le agregan "/docs" al final de esta manera ""http://127.0.0.1:8000"/docs"

5. Les aparecera la pagina de fastapi con los endpoints que podran ejecutar cuando desplieguen en la parte de la derecha de cada uno de ellos para luego hacer click en execute

6. Como funciona cada endpoint

- POST/seed-aeropuertos: crea los dos aeropuertos que estan en el main
- POST/seed-vuelos: crea los dos vuelos que estan de prueba en el main
- GET/itinerarios: lista los itinerarios con los vuelos que que tienen un numero de vuelo, un origen y un destino con su respectivo aeropuerto, tambien que tipo es y en que estado se encuentra
- DELETE/vuelos{vuelo_id}: Borra los vuelos por su id
- DELETE/aeropuertos{aeropuertos_id}: Borra los aeropuertos por su id y verifica si tiene vuelos asociados
- GET/test-db: Es un endpoint de prueba para ver si funcionaba el fastapi