from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import jwt_auth_user, usuario, restaurante
from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:80"  # Cambia este origen si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routers
app.include_router(usuario.router)
app.include_router(jwt_auth_user.router)
app.include_router(restaurante.router)

@app.get("/")
async def root():
    return "hola mundo"