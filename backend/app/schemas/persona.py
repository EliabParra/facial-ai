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
    # La lista de fotos en base64 se valida en la ruta, aquí definimos los datos de DB.
    pass


class PersonaResponse(PersonaBase):
    id: int
    
    # Excluimos embeddings por default en la respuesta para no enviar arrays inmensos al cliente
    
    class Config:
        from_attributes = True
