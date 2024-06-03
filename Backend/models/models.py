from sqlalchemy import Column, Integer, String, Boolean
from Backend.config.bd import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    ci = Column(Integer, primary_key=True, index=True) 
    nombre = Column(String(40))
    apellido = Column(String(40))
    email = Column(String(100), unique=True)
    contrasena = Column(String(556))