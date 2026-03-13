"""
Schemas Pydantic para el modelo Persona.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr


class PersonaCreate(PersonaBase):
    # Lista de fotos en base64 para el registro.
    # El usuario debe enviar al menos 1 foto.
    fotos: list[str]


class PersonaResponse(PersonaBase):
    id: int
    
    # Excluimos embeddings por default en la respuesta para no enviar arrays inmensos al cliente
    
    class Config:
        from_attributes = True
