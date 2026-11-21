from sqlalchemy import Column, Integer, Numeric, String, Boolean, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from src.db.session import Base


class Product(Base):

    # Nombre de la tabla
    __tablename__ = 'products'

    # Definicion de reglas
    __table_args__ = (
        CheckConstraint('stock >= 0', name='ck_products_stock_non_negative'),
    )

    # Columnas
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'), index=True)

    # Traer registro de la categoria a la que pertenece el producto
    category = relationship('Category')
    