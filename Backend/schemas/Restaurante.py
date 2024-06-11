from pydantic import BaseModel
import datetime

class RestauranteBase(BaseModel):
    nombre: str
    calle: str
    esquina: str
    reserva_max: int
    imagen: str
    calificacion: float
    tipo: str
    precio: int
    telefono: int
    google: str
    hora_inicio: datetime.time
    hora_fin: datetime.time
    descripcion: str  

class RestauranteBDBase(RestauranteBase):
    id_restaurante: int

class RestauranteHorarioBase(BaseModel):
    id_restaurante: int
    hora: int
