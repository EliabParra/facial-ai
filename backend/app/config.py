"""
Configuración central de la aplicación.

Centraliza variables de entorno y constantes para evitar
valores hardcodeados dispersos en el código.
"""

import os


# Base de datos
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:////data/database.db")

# CORS — Orígenes permitidos
CORS_ORIGINS: list[str] = [
    "http://localhost:5173",
    "http://frontend:5173",
]

# DeepFace — Configuración de modelos
FACE_MODEL: str = "VGG-Face"            # Modelo para embeddings faciales
EMOTION_DETECTOR: str = "emotion"        # Acción de DeepFace para emociones

# WebSocket — Control de rendimiento
WS_MAX_FPS: int = 10                     # Máximo de frames por segundo procesados
WS_JPEG_QUALITY: int = 60               # Calidad de compresión JPEG (0-100)

# Reconocimiento — Umbrales
SIMILARITY_THRESHOLD: float = 0.6        # Umbral de distancia coseno para match
