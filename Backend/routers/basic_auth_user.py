from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    name: str
    surname: str
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "gaspar": {
        "name": "gaspar",
        "surname": "Morales",
        "email": "gmorales1@gmail.com",
        "disable": False,
        "password": "123456"
    },
    "gaspar2": {
        "name": "gaspar2",
        "surname": "Morales2",
        "email": "gmorales2@gmail.com",
        "disable": True,
        "password": "654321"
    }
}

def search_userDB(name: str):
    if name in users_db:
        return UserDB(**users_db[name])

def search_user(name: str):
    if name in users_db:
        return User(**users_db[name])

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="credenciales de authenticacion invalidas", headers={"WWW-Authenticate": "Bearer"})
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")
    user = search_userDB(form.username)
    if user.password != form.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    return {"access_token": user.name, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user