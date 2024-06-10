from fastapi import APIRouter, HTTPException, Depends, status
from typing import Annotated
from schemas.Restaurante import RestauranteBase, RestauranteBDBase, RestauranteHorarioBase
from schemas.Usuario import UsuarioDBBase
from models import models
from config.bd import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_
import pika
import json
import os


router = APIRouter(responses={404: {"message": "No encontrado"}},
                   tags=["Reserva"])

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/verreservas/{id_restaurante}")
async def get_reservas(id_restaurante: int, db: db_dependency):
    try:
        return db.query(models.Reserva).filter(models.Reserva.id_restaurante == id_restaurante)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="bd Caida")

@router.post("/hacerreserva")
async def create_reserva(email: str, idrestaurante: int, hora: int, fecha: str, numsillas: int, db: db_dependency):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).all()
    restaurante = db.query(models.Restaurante).filter(models.Restaurante.id_restaurante == idrestaurante).all()
        
    nombreusuario = email
    if not len(usuario) == 0:
        nombreusuario = usuario[0].nombre
    
    direccion = restaurante[0].calle + ' esquina ' + restaurante[0].esquina
    
    nombrerestaurante = restaurante[0].nombre
    
    publish_message(email, nombreusuario, numsillas, nombrerestaurante, direccion, hora, fecha)


def publish_message(email: str, nombreusuario: str, numsillas: int, nombrerestaurante: str, direccion: str, hora: int, fecha: str):
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue='Reservations')

    datos_reserva = {
        "nombreusuario": nombreusuario,
        "email": email,
        "nombrerestaurante": nombrerestaurante,
        "direccion": direccion,
        "hora": hora,
        "fecha": fecha,
        "cantidad_sillas": numsillas
    }
    
    message = json.dumps(datos_reserva)
    channel.basic_publish(exchange='', routing_key='Reservations', body=message)

    print(" [x] Sent 'Reservation made'")
    connection.close()