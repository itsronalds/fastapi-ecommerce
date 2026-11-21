from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):

    name: str = Field(min_length=3, max_length=255)
    description: Optional[str]
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    category_id: Optional[int]


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):

    name: Optional[str] = Field(default=None, min_length=3, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(gt=0, max_digits=10, decimal_places=2)
    stock: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int]
    is_active: Optional[bool] = None
    