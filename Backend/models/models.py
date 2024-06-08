from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Double
from sqlalchemy.orm import relationship
from config.bd import Base

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
    
    imagen = Column(String(250))
    rating = Column(Double)
    precio = Column(Integer)
    tipo = Column(String(50))


class RestauranteHora(Base):
    __tablename__ = 'restauranteHora'
    
    id_restaurante = Column(Integer, primary_key=True, nullable=False)
    hora = Column(Integer, primary_key=True, nullable=False)

"""class Reserva(Base):
    __tablename__ = 'reserva'
    
    rest = None
    email = None
    
    id_reserva = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_reservado = Column(String(190))
    id_restaurante = Column(Integer)
    hora = Column(Integer, nullable=False)
    fecha = Column(DateTime, nullable=False)
    num_silla = Column(Integer, nullable=False)"""
