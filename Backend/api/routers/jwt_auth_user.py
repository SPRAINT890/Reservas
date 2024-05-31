from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "9dfceeac69eb3c827ee4468fea7150b7a054d1ae3a54cb2c012e0226a5e15d2c"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

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
        "password": "$2a$12$fzlxGTHY2kcdSEyhR7zyPOEz6YapTs1qaPFkP8mcqLb6ZwklrL14O"
    },
    "gaspar2": {
        "name": "gaspar2",
        "surname": "Morales2",
        "email": "gmorales2@gmail.com",
        "disable": True,
        "password": "$2a$12$kkRZpiZN4RBe5Hwb6n7l2.C07R3I.s1tyvpOjSm61I43eTWf1BaWy"
    }
}

def search_userDB(name: str):
    if name in users_db:
        return UserDB(**users_db[name])

def search_user(name: str):
    if name in users_db:
        return User(**users_db[name])

async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="credenciales de authenticacion invalidas", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="El usuario no es correcto")

    user = search_userDB(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    

    access_token = {"sub": user.name, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

