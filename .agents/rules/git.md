# Convenciones de Git y Control de Versiones

Reglas de ramas, mensajes de commit e higiene del repositorio para `fastapi-ecommerce`.

## Flujo de ramas (*Branching Strategy*)

- **`main`** es la rama principal y debe mantenerse siempre en estado funcional y desplegable.
- No trabajar funcionalidades grandes ni refactorizaciones directamente sobre `main`; crear una rama dedicada desde `main` actualizada e integrar mediante Pull Request.

### Nomenclatura de ramas

Formato: `<type>/<short-kebab-case-description>`

| Prefijo | Uso | Ejemplo |
|---|---|---|
| `feat/` | Nueva funcionalidad o endpoint | `feat/orders-crud` |
| `fix/` | Corrección de errores | `fix/category-http-exception` |
| `refactor/` | Mejora interna sin cambiar comportamiento externo | `refactor/products-service-layer` |
| `docs/` | Documentación o reglas | `docs/agent-rules` |
| `test/` | Pruebas unitarias o de integración | `test/orders-stock-validation` |
| `chore/` | Mantenimiento, dependencias, configuración | `chore/update-requirements` |

---

## Conventional Commits (en inglés)

Todos los mensajes de commit deben seguir [Conventional Commits](https://www.conventionalcommits.org/) en **inglés**:

```text
<type>(<optional-scope>): <short description>
```

### Tipos permitidos

- `feat`: nueva funcionalidad para el usuario o la API.
- `fix`: corrección de un bug.
- `refactor`: reestructuración de código que no añade funcionalidad ni corrige un bug.
- `docs`: cambios en documentación (`README.md`, `docs/`, `AGENTS.md`, `.agents/rules/`).
- `test`: creación o actualización de pruebas.
- `chore`: tareas de mantenimiento, dependencias (`requirements.txt`), archivos de entorno (`.env.example`), configuración.
- `style`: cambios de formato que no afectan la lógica (espacios, orden de imports).
- `perf`: mejoras de rendimiento.
- `build` / `ci`: cambios en empaquetado o pipelines de integración continua.

> **Nota sobre historial previo:** En commits iniciales se usó `add:` (ej. `add: .env.example`). A partir de esta regla, reemplázalo por `feat:`, `chore:` o `docs:` según corresponda.

### Reglas de redacción

1. Usar **modo imperativo en presente** y en inglés (`add`, `fix`, `update`, `remove`, no `added` ni `adding`).
2. Comenzar la descripción en **minúscula** y **sin punto final**.
3. Mantener la primera línea por debajo de **72 caracteres**.
4. Usar `<scope>` cuando aporte claridad (`products`, `categories`, `orders`, `db`, `config`, `rules`).
5. Si el cambio requiere contexto adicional (el "por qué" o un *breaking change*), añadir cuerpo separado por una línea en blanco.

### Ejemplos

```text
# Correctos
feat(orders): add order creation with stock validation
fix(categories): replace raise JSONResponse with HTTPException
refactor(products): migrate routes to service and repository layers
docs(rules): add architecture and code style guidelines
chore(db): add DATABASE_URL placeholder to .env.example

# Incorrectos
add: orders                          # Tipo no estándar
feat: Added category endpoints.      # Pasado, mayúscula y punto final
fix stuff                            # Sin tipo ni contexto
```

---

## Higiene de commits y Pull Requests

- **Commits atómicos:** cada commit debe representar un cambio lógico completo y coherente. No mezclar refactorizaciones no relacionadas con features o fixes en el mismo commit.
- **Archivos prohibidos en Git:** nunca commitear `.env`, `venv/`, `__pycache__/`, credenciales, dumps de base de datos ni archivos temporales. Verificar con `git status` y `git diff --staged` antes de commitear.
- **Verificación previa al commit:**
  1. Confirmar que los imports resuelven sin errores y que la aplicación inicia correctamente.
  2. Verificar que no haya código comentado innecesario ni `print()` de depuración.
  3. Ejecutar las pruebas relacionadas si existen.
- **Pull Requests:**
  - Título en formato Conventional Commit.
  - Descripción breve indicando qué cambia, por qué y cómo se probó (endpoints probados en `/docs` o pruebas ejecutadas).
  - Preferir **Squash and merge** al integrar en `main` para conservar un historial lineal y limpio.
