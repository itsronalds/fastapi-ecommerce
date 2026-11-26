# Guía de Estilo de Código

Reglas de estilo para escribir código limpio, consistente y idiomático en Python 3.11+, FastAPI, Pydantic v2 y SQLAlchemy 2.x.

## Python general (PEP 8)

- **Versión objetivo:** Python 3.11+.
- **Indentación:** 4 espacios (nunca tabs).
- **Longitud máxima de línea:** 88 a 100 caracteres.
- **Codificación y fin de archivo:** UTF-8 y siempre terminar cada archivo con un salto de línea (`\n`). Sin espacios en blanco al final de línea (*trailing whitespace*).
- **Comillas:** usar comillas simples (`'...'`) de forma consistente en strings de código (alineado con el proyecto actual) y comillas dobles triples (`"""..."""`) para docstrings.
- **Código muerto:** no dejar código comentado, `print()` de depuración ni imports sin usar.

## Organización de imports

Usar siempre **imports absolutos** desde `src.` y agruparlos en tres bloques separados por una línea en blanco:

1. Librería estándar de Python (`decimal`, `logging`, `pathlib`, `typing`).
2. Librerías de terceros (`fastapi`, `pydantic`, `sqlalchemy`).
3. Módulos locales (`src.core`, `src.db`, `src.models`, `src.repositories`, `src.schemas`, `src.services`).

```python
from decimal import Decimal
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.category import CategoryCreate, CategoryRead
from src.services import category as category_service
```

## Tipado estático (*Type Hints*)

- Todas las funciones, métodos y endpoints deben incluir anotaciones de tipo en parámetros y valor de retorno.
- Preferir sintaxis nativa de Python 3.11+:
  - `list[Product]` en lugar de `List[Product]`.
  - `Product | None` (o `Optional[Product]` si se mantiene consistencia dentro del mismo archivo existente).
  - Evitar `dict` sin tipar cuando se conozca la estructura; preferir `dict[str, Any]` o pasar directamente el schema Pydantic al servicio.

## FastAPI

- **Parámetros de ruta:** el nombre del parámetro en el decorador **debe coincidir exactamente** con el argumento de la función:
  ```python
  # Correcto
  @router.get('/{category_id}', response_model=CategoryRead)
  def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryRead:
      ...

  # Incorrecto: '/{id}' con parámetro 'category_id' provoca que FastAPI lo trate como query param
  ```
- **Manejo de errores:** usar siempre `raise HTTPException(status_code=..., detail=...)` con constantes de `fastapi.status`.
  - **Nunca** hacer `raise JSONResponse(...)` (es un error en tiempo de ejecución porque `JSONResponse` no hereda de `BaseException`).
  - **No** mezclar `return JSONResponse(...)` para errores en endpoints tipados con `response_model`.
- **Códigos de estado explícitos:** declarar `status_code=status.HTTP_201_CREATED` en endpoints `POST` de creación.
- **Instancias `APIRouter`:** definir `prefix` y `tags` en el router de cada recurso para evitar repetir el prefijo en cada decorador.

## Pydantic v2

- En esquemas de lectura (`*Read`), habilitar lectura desde modelos ORM con:
  ```python
  model_config = ConfigDict(from_attributes=True)
  ```
- En campos opcionales, **siempre asignar `= None`** (o `Field(default=None, ...)`). En Pydantic v2, escribir `description: Optional[str]` sin default hace que el campo sea obligatorio aunque acepte `None`.
- Para valores monetarios (`price`, `total`), usar siempre `Decimal` con `Field(gt=0, max_digits=10, decimal_places=2)`, nunca `float`.
- Para actualizaciones parciales (`*Update`), extraer solo los campos enviados por el cliente usando `payload.model_dump(exclude_unset=True)`.

## SQLAlchemy 2.x

- Usar exclusivamente la API 2.x (`select(...)`, `db.scalars(...)`, `db.scalar(...)`, `db.get(...)`). No usar la API legacy `db.query(...)`.
- Materializar siempre colecciones antes de devolverlas:
  ```python
  # Correcto
  return list(db.scalars(select(Product).order_by(Product.id)))

  # Incorrecto: devuelve un objeto ScalarResult consumible una sola vez
  return db.scalars(select(Product).order_by(Product.id))
  ```
- Usar `db.refresh(entity)` después de `commit()` cuando se necesite leer campos generados o actualizados por la base de datos.
- Definir restricciones de integridad (`CheckConstraint`, `ForeignKey`, `unique=True`, `index=True`) directamente en el modelo ORM.

## Comentarios, docstrings y logging

- Escribir docstrings y comentarios en **español**.
- Los comentarios deben explicar el **por qué** de una decisión no obvia, no repetir literalmente lo que hace la siguiente línea de código.
- Para trazas en ejecución, usar `logger = logging.getLogger(__name__)`. Reservar `print()` únicamente para scripts CLI independientes como `src/db/init_db.py`.
