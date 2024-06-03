#datos obligatorio usar path
#datos no obligatorio user query

from fastapi import APIRouter, HTTPException, Depends, status #framework (se necesita instalar modulo)
from fastapi.responses import HTMLResponse #Codigo de respuestas de http
from typing import Annotated
import aiofiles #para leer archivos ej, leer el front (se necesita instalar modulo)
from Backend.schemas.Usuario import UsuarioDBBase, UsuarioBase
from cryptography.fernet import Fernet
from Backend.models import models
from Backend.config.bd import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter(responses={404: {"message": "No encontrado"}},
                   tags=["Usuarios"])

key = Fernet.generate_key()
f = Fernet(key)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(get_db)]

#devuelve todos los usuarios
@router.get('/users')
async def get_users(db: db_dependency):
    return db.query(models.Usuario).all()

def search_user_ci(ci: int, db: db_dependency):
    return db.query(models.Usuario).filter(models.Usuario.ci == ci).first()

def search_user_email(email: int, db: db_dependency):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

#agregar usuario
@router.post("/register/newuser", status_code=status.HTTP_201_CREATED)
async def create_user(newuserraw: UsuarioDBBase, db: db_dependency):
    raw = {"ci": newuserraw.ci, 
            "nombre": newuserraw.nombre,
            "apellido": newuserraw.apellido,
            "email": newuserraw.email,
            "contrasena": f.encrypt(newuserraw.contrasena.encode("utf-8"))}
    
    #datos repetidos
    if search_user_ci(newuserraw.ci, db) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cedula en uso")
    if search_user_email(newuserraw.email, db) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email en uso")
    
    #crear usuario
    newuser = models.Usuario(**raw)
    db.add(newuser)
    db.commit()

"""#devuelve el usuario con id
@router.get("/user/{id}") #usuario por path
async def user(id: int):
    return search_user_ci(id)

@router.get("/userquery/") #paramentro por query ?id=1
async def userquery(id: int):
    return search_user_ci(id)"""
"""
#modificar usuario
@router.put("/user/", status_code=202)
async def user(user: UsuarioDBBase):
    if type(search_user(user.id)) != UsuarioDBBase:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    for index, usersaved in enumerate(userslist):
        if usersaved.id == user.id:
            userslist[index] = user
            return "ok"

#borrar
@router.delete("/user/{id}", status_code=202)
async def user(id: int):
    if type(search_user(id)) != UsuarioDBBase:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    for index, usersaved in enumerate(userslist):
        if usersaved.id == id:
            del userslist[index]
            return "usuario borrado"
"""