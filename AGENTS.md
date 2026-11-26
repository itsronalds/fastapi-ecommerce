# AGENTS.md — FastAPI E-commerce API

## Stack

- **Lenguaje:** Python 3.11+
- **Framework API:** FastAPI + Uvicorn
- **Validación y configuración:** Pydantic v2 + `pydantic-settings`
- **ORM:** SQLAlchemy 2.x
- **Base de datos:** PostgreSQL (`psycopg` 3)

## Reglas del proyecto

Antes de diseñar, modificar código o crear commits, consulta y cumple estas reglas:

- **[.agents/rules/architecture.md](.agents/rules/architecture.md):** Arquitectura por capas, manejo de sesiones, transacciones y límites de responsabilidad.
- **[.agents/rules/code-style.md](.agents/rules/code-style.md):** Estilo de Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.x, tipado y logging.
- **[.agents/rules/conventions.md](.agents/rules/conventions.md):** Convenciones de nombres, idioma, diseño REST, códigos HTTP, manejo de errores con `HTTPException`, variables de entorno y testing.
- **[.agents/rules/git.md](.agents/rules/git.md):** Flujo de ramas, Conventional Commits en inglés, higiene de commits y Pull Requests.

## Principios del proyecto

1. **Respeta la separación de capas:** Las rutas solo gestionan HTTP; la lógica de negocio y validaciones de dominio viven en `src/services/`; el acceso a base de datos vive en `src/repositories/`.
2. **Errores HTTP estándar:** Usa `raise HTTPException(status_code=..., detail=...)` con mensajes claros en español. Nunca uses `raise JSONResponse(...)`.
3. **Integridad de datos y dinero:** Usa `Decimal` (`Numeric(10, 2)`) para precios y totales, nunca `float`. Operaciones multi-paso (ej. crear orden y descontar stock) deben ser atómicas dentro de una misma transacción.
4. **Seguridad y configuración:** Nunca hardcodees credenciales ni commitees `.env`. Toda variable de entorno nueva debe agregarse en `.env.example` y en `src/core/config.py`.
5. **Idioma:** Código, identificadores, rutas URL y commits en **inglés**; documentación, comentarios, docstrings y mensajes de error de la API en **español**.
6. **Verificación antes de concluir:** Revisa imports, tipos, consistencia de rutas/schemas y comportamiento esperado antes de reportar una tarea como completada.
