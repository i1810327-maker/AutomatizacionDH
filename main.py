from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import seed, login, docente, directora


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(seed.router)
app.include_router(login.router)
app.include_router(docente.router)
app.include_router(directora.router)


@app.get("/")
def saludar():
    return {"mensaje": "Bienvenido a FastAPI"}
