"""Prácticas 1 y 2 · API de Órdenes con FastAPI."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from . import models  # noqa: F401
from .db import Base, engine
from app.routers.orders import router as orders_router
from app.routers.web import router as web_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ejecuta acciones al iniciar y cerrar el servidor."""
    Base.metadata.create_all(engine)
    logger.info("API de Órdenes iniciada")
    yield
    logger.info("API de Órdenes detenida")


app = FastAPI(
    title="API de Órdenes",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(orders_router)
app.include_router(web_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Verifica que el servidor está vivo."""
    return {"status": "ok"}


@app.get("/saludo/{nombre}")
def saludar(nombre: str, mayusculas: bool = False) -> dict[str, str]:
    """`nombre` es parámetro de ruta; `mayusculas` es parámetro de query."""
    mensaje = f"Hola, {nombre}"
    if mayusculas:
        mensaje = mensaje.upper()
    return {"mensaje": mensaje}


@app.get("/cuadrado/{n}")
def cuadrado(n: int) -> dict[str, int]:
    """FastAPI convierte y valida `n` gracias al type hint `int`."""
    return {"n": n, "cuadrado": n * n}