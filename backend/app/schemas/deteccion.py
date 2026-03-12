"""
Schemas Pydantic para el modelo Deteccion.
"""

from pydantic import BaseModel
from datetime import datetime


class DeteccionBase(BaseModel):
    emocion_detectada: str
    confianza: float


class DeteccionCreate(DeteccionBase):
    persona_id: int


class DeteccionResponse(DeteccionCreate):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
