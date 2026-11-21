from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.product import Product


def get_all(db: Session) -> list[Product]:
    """Obtener todas las productos"""

    # SELECT * FROM categories ORDER BY id
    return db.scalars(select(Product).order_by(Product.id))


def get_by_id(db: Session, product_id: int) -> Optional[Product]:
    """Obtener producto por id"""

    return db.get(Product, product_id) 


def create(db: Session, data: dict) -> Product:
    """Crear nueva producto"""
    # product_1 = {
    #     'id': '',
    #     'name': ''
    # }
    # # id, name 
    # product_2 = {
    #     **product_1,
    #     'is_active': True
    # }
    # # id, name, is_active

    product = Product(**data, is_active=True)
    
    # Equivalente a insert
    db.add(product)

    # Confirmacion de registro en base de datos
    db.commit()

    # Retorna producto creado
    return product


def update(db: Session, product: Product, changes: dict) -> Product:
    """Actualizar producto"""

    # Iterar cambios que vienen del front y hacer el update en base de datos
    for key, value in changes.items():
        setattr(product, key, value)
    db.commit()
    return product


def delete(db: Session, product: Product) -> None:
    """Eliminar categoria"""

    db.delete(product)
    db.commit()
