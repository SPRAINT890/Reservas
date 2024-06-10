from typing import Optional
from pydantic import BaseModel #para hacer clases
from datetime import date

class ReservaDBBase(BaseModel):
    id_reserva: int
    email_reservado: str
    hora: int
    fecha: date
    num_silla: int