from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from Backend.schemas.Restaurante import RestauranteBase
from Backend.models import models
from Backend.config.bd import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_

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

@router.get("/busqueda/{calle}", status_code=status.HTTP_202_ACCEPTED)
async def get_restaurante(direccion: str, db: db_dependency):
    return db.query(models.Restaurante).filter(or_(models.Restaurante.esquina == direccion, models.Restaurante.calle == direccion)).all()

@router.post("/agregarrestaurante", status_code=status.HTTP_201_CREATED)
async def add_restaurant(newrestaurantraw: RestauranteBase, db: db_dependency):
    newrestaurant = models.Restaurante(**newrestaurantraw.model_dump())
    db.add(newrestaurant)
    db.commit()