from fastapi import FastAPI
from .routers import jwt_auth_user, usuario, restaurante
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(usuario.router)
app.include_router(jwt_auth_user.router)
app.include_router(restaurante.router)
app.mount("/static", StaticFiles(directory='Backend/static'), name="static")

@app.get("/")
async def root():
    return "hola mundo"