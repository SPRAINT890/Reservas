from typing import Optional
from pydantic import BaseModel #para hacer clases

class UserDB(BaseModel):
    ci: int
    nombre: str
    apellido: Optional[str]
    email: str
    contraseña: str