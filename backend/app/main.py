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
from app.routers import personas, reconocimiento, reportes

# Crea las tablas si no existen en SQLite
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Facial-AI API",
    description="Sistema de Reconocimiento Facial con Análisis de Emociones",
    version="0.1.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar routers
app.include_router(personas.router)
app.include_router(reconocimiento.router)
app.include_router(reportes.router)


@app.get("/", tags=["Health"])
async def health_check() -> dict:
    """Endpoint de verificación de salud del servicio."""
    return {
        "status": "ok",
        "service": "facial-ai-backend",
        "version": "0.1.0",
    }
