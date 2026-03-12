"""
Modelo SQLAlchemy para la tabla Personas.
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Campo TEXT para almacenar el JSON string del embedding generado por DeepFace.
    embeddings = Column(Text, nullable=False)
    
    # Relación uno-a-muchos con detecciones
    detecciones = relationship("Deteccion", back_populates="persona", cascade="all, delete-orphan")
