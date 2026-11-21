from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):

    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int 