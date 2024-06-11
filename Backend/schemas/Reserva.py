from typing import Optional
from pydantic import BaseModel #para hacer clases
from datetime import date

class ReservaBase(BaseModel):
    email_reservado: str
    id_restaurante: int
    hora: int
    fecha: date
    num_silla: int

class ReservaDBBase(ReservaBase):
    id_reserva: int