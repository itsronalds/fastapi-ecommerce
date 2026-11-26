# Tareas del proyecto (Milestones)

Guía de actividades para ampliar la API de E-commerce con **usuarios**, **autenticación con JWT** y **órdenes de compra**.

> **Recordatorio general:** por cada recurso nuevo que creen, recuerden registrar los modelos en `src/models/__init__.py` (para que SQLAlchemy cree las tablas), crear su repositorio en `src/repositories/` (como en `category.py` y `product.py`) y registrar las rutas en `src/routes/__init__.py`.

---

## Milestone 1: Usuarios y autenticación

### 1.1. Crear el modelo de usuario (`src/models/user.py`)

| Campo | Tipo | Reglas |
|---|---|---|
| `id` | `int` | Primary Key, autoincremental |
| `email` | `varchar(255)` | Único, obligatorio (`not null`) |
| `hashed_password` | `varchar(255)` | Obligatorio (`not null`) |
| `role` | `varchar(50)` | Obligatorio (`not null`), valores permitidos: `user` o `admin` (default: `user`) |
| `created_at` | `timestamp` | Obligatorio (`not null`), default: fecha y hora actual |

### 1.2. Crear los schemas (`src/schemas/user.py`)

Crear los schemas y validaciones con **Pydantic** para:
- **Registro y login:** recibir `email` (validar formato de correo con `EmailStr`) y `password` (validar un mínimo de caracteres, por ejemplo 6 u 8).
- **Respuesta de usuario:** devolver `id`, `email`, `role` y `created_at` (nunca devolver la contraseña).
- **Respuesta de login:** devolver el token JWT.

### 1.3. Crear las rutas de autenticación

- **`POST /register`:** crea un usuario nuevo.
  - El cliente solo envía `email` y `password`.
  - El `role` siempre se asigna desde el backend como `user`.
  - Si el `email` ya existe, responder con un error claro (`409` o `400`).
  - La contraseña debe encriptarse antes de guardarse usando [bcrypt](https://pypi.org/project/bcrypt/).
- **`POST /login`:** inicia sesión.
  - El cliente envía `email` y `password`.
  - Validar que el usuario exista y comparar la contraseña con `bcrypt`.
  - Si los datos son correctos, generar y devolver un JWT (por ejemplo con [PyJWT](https://pypi.org/project/PyJWT/)) que incluya fecha de expiración (`exp`).
  - > **Seguridad:** la clave secreta del JWT no debe escribirse fija en el código; guárdenla en `.env` (y agréguenla a `.env.example` y `src/core/config.py`).

---

## Milestone 2: Middleware de JWT y rutas protegidas

### 2.1. Crear la validación de autenticación (`src/middlewares/auth.py`)

- Crear la carpeta `src/middlewares/` y dentro el archivo `auth.py`.
- Investigar e implementar la validación de JWT para integrarla en las rutas de FastAPI cada vez que llegue una solicitud.
- Extraer el token del header `Authorization: Bearer <token>`, verificar que sea válido y no haya expirado, y obtener los datos del usuario autenticado (como su `id` y `role`).
- > **Pista:** en lugar de un middleware global que bloquee `/login`, `/register` o `/docs`, pueden implementarlo como una dependencia reutilizable con `Depends` y `HTTPBearer`. Así solo se aplica a las rutas protegidas y habilita el botón **Authorize** en `/docs`.

### 2.2. Proteger rutas por rol

- Proteger las rutas de creación, edición y eliminación de `categories` y `products` para que **solo usuarios con rol `admin`** puedan ejecutarlas.
- Si el usuario no envía token o el token es inválido/expirado, responder con `401`.
- Si el usuario no tiene rol `admin`, responder con `403`.

### 2.3. Crear un único usuario `admin`

Como `/register` siempre crea usuarios con rol `user`, pueden crear y luego promover un usuario con el rol de `user` a `admin` manualmente en PostgreSQL:

```sql
UPDATE users SET role = 'admin' WHERE id = <Aquí colocan el id del usuario que quiere volver admin>
```

---

## Milestone 3: Órdenes de compra

### 3.1. Crear el modelo de órdenes (`src/models/order.py`)

| Campo | Tipo | Reglas |
|---|---|---|
| `id` | `int` | Primary Key, autoincremental |
| `user_id` | `int` | Foreign Key (`users.id`), obligatorio (`not null`) |
| `status` | `varchar(50)` | Obligatorio (`not null`), default: `pending` (ej: `pending`, `paid`, `cancelled`) |
| `total_amount` | `decimal(10, 2)` | Obligatorio (`not null`) |
| `created_at` | `timestamp` | Obligatorio (`not null`), default: fecha y hora actual |

### 3.2. Crear el modelo de ítems de orden (`src/models/order_item.py`)

| Campo | Tipo | Reglas |
|---|---|---|
| `id` | `int` | Primary Key, autoincremental |
| `order_id` | `int` | Foreign Key (`orders.id`), obligatorio (`not null`) |
| `product_id` | `int` | Foreign Key (`products.id`), obligatorio (`not null`) |
| `quantity` | `int` | Obligatorio (`not null`), mayor que `0` |
| `unit_price` | `decimal(10, 2)` | Obligatorio (`not null`) — precio del producto al momento de la compra |

> **Nota:** agregar una restricción única combinada `(order_id, product_id)` para evitar que el mismo producto se repita dos veces dentro de la misma orden.

### 3.3. Crear los schemas (`src/schemas/order.py`)

Crear los schemas y validaciones con **Pydantic** para:
- **`OrderItemCreate`:** recibe `product_id` y `quantity` (validar que `quantity > 0`).
- **`OrderCreate`:** recibe una lista de `items` (validar que la lista no esté vacía).
- **`OrderItemRead`:** devuelve `id`, `product_id`, `quantity` y `unit_price`.
- **`OrderRead`:** devuelve `id`, `user_id`, `status`, `total_amount`, `created_at` y la lista de `items`.

### 3.4. Crear las rutas de órdenes (`src/routes/orders.py`)

Todas las rutas de órdenes requieren que el usuario esté autenticado con JWT:

- **`POST /orders`:** crea una nueva orden para el usuario autenticado (el `user_id` se toma del token, no lo envía el cliente).
  - Validar que no vengan `product_id` repetidos en `items` (rechazar con `400`, o sumar sus cantidades antes de guardar).
  - Validar que cada producto exista y esté activo (`is_active = True`).
  - Validar que haya suficiente `stock` para la `quantity` solicitada.
  - Guardar el precio actual de cada producto en `unit_price` y calcular el `total_amount`.
  - Descontar el `stock` de cada producto comprado.
  - > **Importante:** todo debe ocurrir en la misma transacción. Si algún producto falla o no tiene stock, no se guarda la orden ni se modifica el stock.
- **`GET /orders`:** lista las órdenes del usuario autenticado (si el usuario es `admin`, puede ver todas).
- **`GET /orders/{id}`:** muestra el detalle de una orden con sus `items` (solo el dueño de la orden o un `admin` pueden verla).

## Arquitectura de base de datos
<img width="1131" height="807" alt="fastapi-ecommerce" src="https://github.com/user-attachments/assets/a17ae947-009a-45a4-ae10-ce59eac78b9c" />
