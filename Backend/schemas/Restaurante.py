from typing import Optional
from pydantic import BaseModel #para hacer clases

class RestauranteBase(BaseModel):
    nombre: str
    calle: str
    esquina: str
    reserva_max: int
    imagen: str
    calificacion: float
    tipo: str
    precio: int


class RestauranteBDBase(RestauranteBase):
    id_restaurante: int

class RestauranteHorarioBase(BaseModel):
    id_restaurante: int
    hora: int