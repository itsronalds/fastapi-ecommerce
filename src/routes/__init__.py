from fastapi import APIRouter

# Routes
from src.routes.products import router as products_router
from src.routes.categories import router as categories_router

router = APIRouter()
router.include_router(products_router)
router.include_router(categories_router)
