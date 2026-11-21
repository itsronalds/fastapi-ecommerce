import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session 

import src.repositories.category as categories_repo
from src.db.session import get_db
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter(tags=['Categories'])


@router.get('/categories')
def get_categories(db: Session = Depends(get_db)) -> list[CategoryRead]:
    return categories_repo.get_all(db)


@router.get('/categories/{id}')
def get_category(category_id: int, db: Session = Depends(get_db)) -> CategoryRead:
    category = categories_repo.get_by_id(db, category_id)
    if not category:
        return JSONResponse({'message': 'La categoria no existe'}, status_code=404)
    return category


@router.post('/categories')
def create_category(category: CategoryCreate, db: Session = Depends(get_db)) -> CategoryRead:
    if categories_repo.get_by_name(db, category.name):
        return JSONResponse({'message': 'El nombre de la categoria ya existe'}, status_code=409)
    return categories_repo.create(db, category.model_dump())


@router.put('/categories/{id}')
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)) -> CategoryRead:
    # Revisar siel id de categoria existe
    current = categories_repo.get_by_id(db, category_id) 
    if not current:
        raise JSONResponse({'message': 'La categoria a actualizar no existe'}, status_code=404)
    
    # Pasar de pydantic a dict
    changes = category.model_dump(exclude_unset=True)

    # Validar que el nombre de categoria venga en el request
    if 'name' in changes and changes['name'] is None:
        raise JSONResponse({'message': 'El nombre no puede estar vacio'}, status_code=400)
    
    # Validar que el nuevo nombre no exista
    existing = categories_repo.get_by_name(db, changes['name'])
    if existing and existing.id != category_id:
        raise JSONResponse({'message': 'Ya existe una categoria con ese nombre'}, status_code=400)
    
    return categories_repo.update(db, current, changes)


@router.delete('/categories/{id}')
def delete_category(category_id: int, db: Session = Depends(get_db)) -> dict:
    # Verificar que exista la categoria
    category = categories_repo.get_by_id(db, category_id)
    if not category:
        raise JSONResponse({'message': 'Categoria no encontrada'}, status_code=404)
    
    # Eliminarla de la base de datos
    categories_repo.delete(db, category)

    # Retornar mensaje de existo
    return {'message': 'Categoria eliminada'}
