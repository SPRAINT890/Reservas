from sqlalchemy import Column, Integer, String, Boolean
from Backend.config.bd import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    ci = Column(Integer, primary_key=True, index=True) 
    nombre = Column(String(40))
    apellido = Column(String(40))
    email = Column(String(100), unique=True)
    contrasena = Column(String(556))

class Restaurante(Base):
    __tablename__ = 'restaurante'
    
    id_restaurante = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    calle = Column(String(250), nullable=False, index=True)
    esquina = Column(String(250), nullable=False, index=True)
    reserva_max = Column(Integer, nullable=False)
    