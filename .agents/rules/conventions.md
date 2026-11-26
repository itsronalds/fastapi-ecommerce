# Convenciones del Proyecto

Estándares de nomenclatura, diseño de API REST, idioma, configuración y pruebas para `fastapi-ecommerce`.

## Política de idiomas

| Elemento | Idioma | Ejemplo |
|---|---|---|
| Código (clases, funciones, variables, parámetros) | Inglés | `get_by_id`, `category_id`, `is_active` |
| Tablas, columnas y constraints SQL | Inglés | `categories`, `stock`, `ck_products_stock_non_negative` |
| Rutas URL y llaves JSON | Inglés | `/products/{product_id}/category`, `category_id` |
| Mensajes de error y respuesta de la API | Español | `'La categoría no existe'` |
| Comentarios, docstrings y documentación | Español | `"""Obtiene una categoría por su ID."""` |
| Mensajes de commit y nombres de ramas | Inglés | `feat(orders): add stock validation` |

---

## Convenciones de nombres

### Archivos y carpetas (`snake_case`)
- **Rutas (`src/routes/`):** en **plural** → `products.py`, `categories.py`, `orders.py`.
- **Modelos (`src/models/`):** en **singular** → `product.py`, `category.py`, `order.py`.
- **Schemas (`src/schemas/`):** en **singular** → `product.py`, `category.py`, `order.py`.
- **Repositorios (`src/repositories/`):** en **singular** → `product.py`, `category.py`, `order.py`.
- **Servicios (`src/services/`):** en **singular** → `product.py`, `category.py`, `order.py`.
- **Pruebas (`src/tests/`):** prefijo `test_` → `test_products.py`, `test_categories.py`, `test_orders.py`.

### Clases y funciones
- **Modelos ORM:** `PascalCase` en singular (`Category`, `Product`, `Order`, `OrderItem`).
- **Schemas Pydantic:** sufijo según propósito:
  - `<Entity>Base`: campos comunes compartidos.
  - `<Entity>Create`: payload de creación (`POST`).
  - `<Entity>Update`: payload de actualización (`PUT`/`PATCH`, todos los campos opcionales con default `None`).
  - `<Entity>Read`: representación devuelta por la API (incluye `id` y `ConfigDict(from_attributes=True)`).
- **Funciones de repositorio:** verbos cortos y consistentes (`get_all`, `get_by_id`, `get_by_name`, `create`, `update`, `delete`).
- **Funciones de servicio:** verbos orientados al caso de uso (`list_categories`, `get_category`, `create_category`, `update_category`, `delete_category`, `create_order`).
- **Constantes:** `UPPER_SNAKE_CASE`.

### Base de datos (PostgreSQL)
- **Tablas:** `snake_case` en plural (`categories`, `products`, `orders`, `order_items`).
- **Columnas:** `snake_case` en singular (`id`, `name`, `category_id`, `is_active`, `created_at`).
- **Restricciones con nombre:** prefijos estándar `pk_`, `fk_`, `uq_`, `ck_`, `ix_` (ej. `ck_products_stock_non_negative`).

---

## Diseño de API REST

### Rutas y verbos HTTP
- Recursos siempre en **plural** y `kebab-case` si tienen múltiples palabras.
- Subrecursos anidados cuando expresen pertenencia directa (ej. `GET /products/{product_id}/category`).

| Operación | Método | Ruta ejemplo | Código de éxito |
|---|---|---|---|
| Listar | `GET` | `/categories` | `200 OK` |
| Obtener detalle | `GET` | `/categories/{category_id}` | `200 OK` |
| Crear | `POST` | `/categories` | `201 Created` |
| Actualizar | `PUT` / `PATCH` | `/categories/{category_id}` | `200 OK` |
| Eliminar | `DELETE` | `/categories/{category_id}` | `200 OK` o `204 No Content` |

### Manejo estándar de errores (`HTTPException`)

Todos los errores controlados deben lanzarse con `HTTPException` usando el formato nativo de FastAPI (`{"detail": "..."}`):

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='La categoría no existe',
)
```

| Código | Cuándo usarlo |
|---|---|
| `400 Bad Request` | Regla de negocio incumplida (ej. stock insuficiente, producto inactivo, cantidad inválida). |
| `404 Not Found` | El recurso principal o una referencia relacionada (`category_id`, `product_id`) no existe. |
| `409 Conflict` | Conflicto de unicidad o estado (ej. nombre de categoría ya registrado). |
| `422 Unprocessable Entity` | Errores de validación de esquema (gestionados automáticamente por FastAPI/Pydantic). |

### Registro de routers
- Cada router de recurso define su `prefix` y `tags` (ej. `APIRouter(prefix='/categories', tags=['Categories'])`).
- `src/routes/__init__.py` es el único punto donde se agregan los routers al router raíz.

---

## Configuración y variables de entorno

- Toda configuración sensible o dependiente de entorno (como `DATABASE_URL`) se declara en `Settings` dentro de `src/core/config.py`.
- Nunca versionar el archivo `.env`.
- Cada vez que se agregue una nueva variable de entorno, documentar su clave (sin secretos reales) en `.env.example`.

---

## Pruebas automatizadas

- Usar `pytest` junto con `fastapi.testclient.TestClient` para pruebas de endpoints y pruebas unitarias de servicios.
- Ejecutar siempre las pruebas contra una base de datos de pruebas aislada (nunca contra la base de datos de desarrollo o producción) sobrescribiendo `get_db` con `app.dependency_overrides`.
- Cubrir tanto el camino feliz (*happy path*) como los casos de error clave (`400`, `404`, `409`, `422`), especialmente validaciones de stock y transacciones en órdenes.
