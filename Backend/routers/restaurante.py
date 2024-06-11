from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from schemas.Restaurante import RestauranteBase, RestauranteBDBase, RestauranteHorarioBase
from models import models
from config.bd import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

router = APIRouter(responses={404: {"message": "No encontrado"}},
                   tags=["Restaurantes"])

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/restBusquedaDir/{calle}", status_code=status.HTTP_202_ACCEPTED)
async def get_restaurante_by_location(calle: str, db: db_dependency):
    return db.query(models.Restaurante).filter(or_(models.Restaurante.esquina.contains(calle), models.Restaurante.calle.contains(calle))).all()

@router.get("/restBusquedaNom/{nombre}", status_code=status.HTTP_202_ACCEPTED)
async def get_restaurante_by_name(nombre: str, db: db_dependency):
    return db.query(models.Restaurante).filter(models.Restaurante.nombre.contains(nombre)).all()

@router.get("/restBusqueda/{nombre},{calle}", status_code=status.HTTP_202_ACCEPTED)
async def get_restaurante(nombre: str, calle: str, db: db_dependency):
    if (nombre == "False" and calle ==  "False"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="los datos no tienen valor")
    if (nombre == "False"):
        return await get_restaurante_by_location(calle, db)
    if (calle == "False"):
        return await get_restaurante_by_name(nombre, db)
    return db.query(models.Restaurante).filter(models.Restaurante.nombre.contains(nombre),or_(models.Restaurante.calle.contains(calle),models.Restaurante.esquina.contains(calle))).all()

@router.post("/agregarrestaurante", status_code=status.HTTP_201_CREATED)
async def add_restaurant(newrestaurantraw: RestauranteBase, db: db_dependency):
    newrestaurant = models.Restaurante(**newrestaurantraw.model_dump())
    db.add(newrestaurant)
    db.commit()

@router.post("/agregarhora", status_code=status.HTTP_201_CREATED)
async def add_restaurant_hour(newhourraw: RestauranteHorarioBase, db: db_dependency):
    newhour = models.RestauranteHora(**newhourraw.model_dump())
    db.add(newhour)
    db.commit()