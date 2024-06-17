from typing import Optional
from pydantic import BaseModel #para hacer clases

class UsuarioBase(BaseModel):
    ci: int
    username: str
    nombre: str
    apellido: Optional[str]
    email: str
    contrasena: str

class UsuarioDBBase(UsuarioBase):
    contrasena: str