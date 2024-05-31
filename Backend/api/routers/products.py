from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                   responses={404: {"message": "No encontrado"}},
                   tags=["products"])

productslist = ["p1", "p2", "p3"]

@router.get("/")
async def products():
    return productslist

@router.get("/{id}")
async def products(id: int):
    return productslist[id]