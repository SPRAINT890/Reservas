#datos obligatorio usar path
#datos no obligatorio user query

from fastapi import APIRouter, HTTPException #framework (se necesita instalar modulo)
from pydantic import BaseModel #para hacer clases
from fastapi.responses import HTMLResponse #Codigo de respuestas de http
from sqlalchemy import Table, Column
import aiofiles #para leer archivos ej, leer el front (se necesita instalar modulo)

router = APIRouter(responses={404: {"message": "No encontrado"}},
                   tags=["users"])

#entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

#lista de usarios
userslist = [User(name = "brais", surname = "moure", age = 25, id = 1),
             User(name = "moure", surname = "dev", age = 25, id = 2),
             User(name = "Haakon", surname = "moure", age = 25, id = 3)]

#devuelve todos los usuarios
@router.get("/users")
async def users():
    return userslist

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


#devuelve los usuarios como json
@router.get("/usersjson")
async def usersjson():
    return [{"name": "brais", "surname": "moure"},
            {"name": "moure", "surname": "dev"},
            {"name": "Haakon", "surname": "moure"}]

#agregar usuario
@router.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=400, detail="usuario repetido")
    else:
        userslist.append(user)
        return "agregado"

#modificar usuario
@router.put("/user/", status_code=202)
async def user(user: User):
    if type(search_user(user.id)) != User:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    for index, usersaved in enumerate(userslist):
        if usersaved.id == user.id:
            userslist[index] = user
            return "ok"

#borrar
@router.delete("/user/{id}", status_code=202)
async def user(id: int):
    if type(search_user(id)) != User:
        raise HTTPException(status_code=404, detail="usuario no encontrado")
    for index, usersaved in enumerate(userslist):
        if usersaved.id == id:
            del userslist[index]
            return "usuario borrado"