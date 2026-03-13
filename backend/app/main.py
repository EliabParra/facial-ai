"""
Facial-AI Backend — Punto de entrada principal.

Configura la aplicación FastAPI con CORS, routers y eventos de startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Inicialización de la base de datos
from app.database import engine, Base
import app.models.persona  # noqa
import app.models.deteccion  # noqa

# Router imports
from app.routers import personas

# Crea las tablas si no existen en SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Facial-AI API",
    description="Sistema de Reconocimiento Facial con Análisis de Emociones",
    version="0.1.0",
)

# CORS: Permitir peticiones desde el frontend en desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(personas.router)


@app.get("/", tags=["Health"])
async def health_check() -> dict:
    """Endpoint de verificación de salud del servicio."""
    return {
        "status": "ok",
        "service": "facial-ai-backend",
        "version": "0.1.0",
    }
