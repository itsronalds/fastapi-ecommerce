# FastAPI E-commerce API

REST API para un sistema de E-commerce desarrollada con **FastAPI**, **SQLAlchemy** y **PostgreSQL**. Arquitectura por capas, validación de datos, bases de datos relacionales y autenticación con JWT.

---

## Stack tecnológico

- **Lenguaje:** [Python 3.11+](https://www.python.org/)
- **Framework API:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)
- **Validación y configuración:** [Pydantic v2](https://docs.pydantic.dev/) + `pydantic-settings`
- **ORM:** [SQLAlchemy 2.x](https://www.sqlalchemy.org/)
- **Base de datos:** [PostgreSQL](https://www.postgresql.org/) (`psycopg` 3)

---

## Requisitos previos

- [Python 3.11+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/) instalado y en ejecución
- [Git](https://git-scm.com/)

---

## Instalación y activación del servidor

### 1. Clonar el repositorio

```bash
git clone https://github.com/itsronalds/fastapi-ecommerce.git
cd fastapi-ecommerce
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
```

**Windows (PowerShell / CMD):**
```bash
.\venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto a partir de `.env.example` y configura la conexión a tu base de datos PostgreSQL y agregar la firma de JWT:

```env
DATABASE_URL=postgresql+psycopg://usuario:password@localhost:5432/nombre_bd
JWT_SECRET=xxxxx
```

> Nunca subas tu archivo `.env` al repositorio.

### 5. Crear las tablas en la base de datos

```bash
python -m src.db.init_db
```

### 6. Ejecutar el servidor

Usando `main.py` (inicia en `http://127.0.0.1:8000` con auto reload):

```bash
python main.py
```

O directamente con `uvicorn` (puerto `8000`):

```bash
uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```

---

## Documentación interactiva

Una vez levantado el servidor, puedes probar todos los endpoints desde el navegador:

- **Swagger UI:** `http://127.0.0.1:8000/docs`

---

## Estructura del proyecto

```text
fastapi-ecommerce/
├── docs/                  # Documentación técnica (arquitectura de BD)
├── tasks/                 # Guías y milestones para estudiantes (.md y .pdf)
├── src/
│   ├── app.py             # Instancia principal de FastAPI y registro de rutas
│   ├── core/              # Configuración y variables de entorno (config.py)
│   ├── db/                # Sesión de SQLAlchemy (session.py) e inicialización (init_db.py)
│   ├── models/            # Modelos ORM (tablas de PostgreSQL)
│   ├── repositories/      # Consultas y operaciones contra la base de datos
│   ├── schemas/           # Schemas y validaciones de entrada/salida con Pydantic
│   ├── routes/            # Endpoints agrupados por recurso
│   └── static/            # Archivos estáticos (index.html)
├── main.py                # Punto de entrada para ejecutar Uvicorn
├── .env.example           # Plantilla de variables de entorno
└── requirements.txt       # Dependencias del proyecto
```

---

## Endpoints actuales

| Recurso | Método | Ruta | Descripción |
|---|---|---|---|
| General | `GET` | `/` | Endpoint de prueba (`Hello World`) |
| General | `GET` | `/home` | Devuelve `src/static/index.html` |
| Categorías | `GET` | `/categories` | Lista todas las categorías |
| Categorías | `GET` | `/categories/{id}` | Obtiene una categoría por ID |
| Categorías | `POST` | `/categories` | Crea una categoría |
| Categorías | `PUT` | `/categories/{id}` | Actualiza una categoría |
| Categorías | `DELETE` | `/categories/{id}` | Elimina una categoría |
| Productos | `GET` | `/products` | Lista todos los productos |
| Productos | `POST` | `/products` | Crea un producto |
| Productos | `PUT` | `/products/{product_id}` | Actualiza un producto |
| Productos | `DELETE` | `/products/{product_id}` | Elimina un producto |

---

## Material del curso y actividades

- **Arquitectura de base de datos (DBML / dbdiagram.io):** [docs/db-architecture.md](docs/db-architecture.md)
- **Tareas y Milestones del proyecto:** [tasks/milestones.md](tasks/milestones.md) · [Versión PDF](tasks/milestones.pdf)

---

## Comandos útiles de referencia

```bash
# Instalar FastAPI desde cero
pip install "fastapi[standard]"

# Guardar las dependencias instaladas en requirements.txt (similar a package.json)
pip freeze > requirements.txt

# Crear tablas definidas en src/models/
python -m src.db.init_db

# Levantar servidor manualmente con Uvicorn
uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```
