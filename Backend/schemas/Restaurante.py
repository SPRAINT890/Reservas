from typing import Optional
from pydantic import BaseModel #para hacer clases

class RestauranteBase(BaseModel):
    nombre: str
    calle: str
    esquina: str
    reserva_max: int

class RestauranteBDBase(RestauranteBase):
    id_restaurante: int