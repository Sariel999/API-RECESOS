# API Recesos – Flask

API REST desarrollada con Flask para la gestión de recesos. Permite listar, buscar, crear y actualizar recesos. Incluye documentación interactiva con Swagger (Flasgger).

## Tecnologías
- Python 3
- Flask
- Flask-CORS
- PostgreSQL
- psycopg2-binary
- Pydantic
- Swagger (Flasgger)

## Estructura del proyecto
recesos_api/
│── app.py
│── config.py
│── requerimientos.txt
│── test_db.py
│── .env
│
├── routes/
│ └── recesos.py
│
├── services/
│ └── receso_service.py
│
├── daos/
│ └── receso_dao.py
│
├── schemas/
│ └── receso_schema.py


## Entorno de Python

Crear un entorno virtual:
```bash
python -m venv .venv
Activar el entorno:

Windows (PowerShell):

.venv\Scripts\activate
Linux / Mac:

source .venv/bin/activate
Instalar dependencias:

pip install -r requerimientos.txt
Variables de entorno (.env)
Crear un archivo .env en la raíz del proyecto con la configuración de PostgreSQL:

DB_HOST=localhost
DB_NAME=nombre_base
DB_USER=usuario
DB_PASSWORD=password
DB_PORT=5432
Nota: El archivo .env contiene información sensible y no debe subirse al repositorio.

Ejecución
Iniciar la API:

python app.py
Base URL:

http://127.0.0.1:5000
Endpoints
Health check:

GET /health

Recesos:

GET /recesos

GET /recesos?nombre=ALMUERZO

POST /recesos

PUT /recesos/{id}

Ejemplo de body para POST/PUT:

{
  "id_t": 1,
  "hora_inicio": "08:00:00",
  "hora_fin": "09:00:00",
  "total": "01:00:00",
  "nombre": "ALMUERZO",
  "descripcion": "Receso principal",
  "tipo": "NORMAL"
}
Swagger
Documentación interactiva:

http://127.0.0.1:5000/apidocs/
