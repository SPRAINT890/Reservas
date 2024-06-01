#datos obligatorio usar path
#datos no obligatorio user query

from fastapi import APIRouter, HTTPException #framework (se necesita instalar modulo)
from fastapi.responses import HTMLResponse #Codigo de respuestas de http
import aiofiles #para leer archivos ej, leer el front (se necesita instalar modulo)
from Backend.config.bd import conexionDB
from Backend.models.usuario_table import usuario
from Backend.schemas.Usuario import UserDB
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

router = APIRouter(responses={404: {"message": "No encontrado"}},
                   tags=["usuarios"])

#lista de usarios
userslist = [ ]

#devuelve todos los usuarios
@router.get('/users')
def get_users():
    lista = conexionDB.execute(usuario.select()).fetchall()

    rows = []
    for t in lista:
        ci = t[0]
        nombre = t[1]
        apellido = t[2]
        email = t[3]
        rows.append({"ci": ci, "nombre": nombre, "apellido": apellido, "email": email})
    return rows

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
@router.post("/register/newuser", status_code=201)
async def create_user(newuserraw: UserDB):
    #if type(search_user(user.id)) == UserDB:
    #    raise HTTPException(status_code=400, detail="usuario repetido")
    #else:
    newuser = {"ci": newuserraw.ci, 
               "nombre": newuserraw.nombre,
               "apellido": newuserraw.apellido,
               "email": newuserraw.email,
               "contrasena": f.encrypt(newuserraw.contraseña.encode("utf-8"))}
    resultado = conexionDB.execute(usuario.insert().values(newuser))
    print(resultado)
    return conexionDB.execute(usuario.select())

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