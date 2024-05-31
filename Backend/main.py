from fastapi import FastAPI
from .routers import products, jwt_auth_user, usuario
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(usuario.router)
app.include_router(jwt_auth_user.router)
app.mount("/static", StaticFiles(directory='Backend/static'), name="static")

@app.get("/")
async def root():
    return "hola mundo"