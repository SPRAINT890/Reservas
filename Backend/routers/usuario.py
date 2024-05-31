#datos obligatorio usar path
#datos no obligatorio user query

from fastapi import APIRouter, HTTPException #framework (se necesita instalar modulo)
from fastapi.responses import HTMLResponse #Codigo de respuestas de http
import aiofiles #para leer archivos ej, leer el front (se necesita instalar modulo)
from ..config.BD import conexionDB
from Backend.models.usuario_table import usuario
from ..schemas.Usuario import UserDB
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

router = APIRouter(responses={404: {"message": "No encontrado"}},
                   tags=["users"])

#lista de usarios
userslist = [ ]

#devuelve todos los usuarios
@router.get("/users")
async def get_users():
    return conexionDB.execute(usuario.select()).fetchall

#devuelve el usuario con id
@router.get("/user/{id}") #usuario por path
async def user(id: int):
    return search_user(id)

@router.get("/userquery/") #paramentro por query ?id=1
async def userquery(id: int):
    return search_user(id)

def search_user(id: int):
    user = filter(lambda user: user.id == id, userslist)
    try:
        return list(user)[0]
    except:
        return {"error":"Id no encontrado"}

#agregar usuario
@router.post("/user/", status_code=201)
async def create_user(newuserraw: UserDB):
    #if type(search_user(user.id)) == UserDB:
    #    raise HTTPException(status_code=400, detail="usuario repetido")
    #else:
    newuser = {"ci": newuserraw.ci, 
               "nombre": newuserraw.nombre,
               "apellido": newuserraw.apellido,
               "email": newuserraw.email,
               "contraseña": f.encrypt(newuserraw.contraseña.encode("utf-8"))}
    
    resultado = conexionDB.execute(usuario.insert().values(newuser))
    print(resultado)
    return "agregado"

#modificar usuario
@router.put("/user/", status_code=202)
async def user(user: UserDB):
    if type(search_user(user.id)) != UserDB:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    for index, usersaved in enumerate(userslist):
        if usersaved.id == user.id:
            userslist[index] = user
            return "ok"

#borrar
@router.delete("/user/{id}", status_code=202)
async def user(id: int):
    if type(search_user(id)) != UserDB:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    for index, usersaved in enumerate(userslist):
        if usersaved.id == id:
            del userslist[index]
            return "usuario borrado"