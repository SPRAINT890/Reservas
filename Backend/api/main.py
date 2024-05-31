from fastapi import FastAPI
from .routers import products, user, jwt_auth_user
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers
app.include_router(products.router)
app.include_router(user.router)
app.include_router(jwt_auth_user.router)
app.mount("/static", StaticFiles(directory='Backend/api/static'), name="static")

@app.get("/")
async def root():
    return "hola mundo"