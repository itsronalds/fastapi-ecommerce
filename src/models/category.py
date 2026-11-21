from sqlalchemy import Column, Integer, String, Text

from src.db.session import Base


class Category(Base):
    # Nombre de la tabla
    __tablename__ = 'categories'

    # Columnas
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
