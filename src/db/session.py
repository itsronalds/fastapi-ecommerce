from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.core.config import settings

# Crear motor de la base de datos
engine = create_engine(url=settings.database_url)

# Tienda de sesiones
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# Base para la crescion de tablas
Base = declarative_base()


def get_db() -> Iterator[Session]:
    """Funcion que otorga una sesion por peticion"""
    db = SessionLocal()
    try:
        yield db
    except:
        logger.debug(msg='ERROR DE CONEXION')
    finally:
        db.close()
