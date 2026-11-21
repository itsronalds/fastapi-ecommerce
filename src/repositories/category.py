from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.category import Category


def get_all(db: Session) -> list[Category]:
    """Obtener todas las categorias"""

    # SELECT * FROM categories ORDER BY id
    return list(db.scalars(select(Category).order_by(Category.id)))


def get_by_id(db: Session, category_id: int) -> Optional[Category]:
    """Obtener categoria por id"""

    # SELECT * FROM categories WHERE id = @id
    return db.get(Category, category_id) 


def get_by_name(db: Session, name: str) -> Optional[Category]:
    return db.scalar(select(Category).where(Category.name == name))


def create(db: Session, data: dict) -> Category:
    """Crear nueva categoria"""
    # INSERT INTO (name, description) VALUES ('nombre de categoria', 'pequena descripcion')

    category = Category(**data)
    
    # Equivalente a insert
    db.add(category)

    # Confirmacion de registro en base de datos
    db.commit()

    # Retorna categoria creada
    return category


def update(db: Session, category: Category, changes: dict) -> Category:
    """Actualizar categoria"""

    # Iterar cambios que vienen del front y hacer el update en base de datos
    for key, value in changes.items():
        setattr(category, key, value)
    db.commit()
    return category


def delete(db: Session, category: Category) -> None:
    """Eliminar categoria"""

    db.delete(category)
    db.commit()
