"""
Modelo SQLAlchemy para la tabla Detecciones.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from app.database import Base


class Deteccion(Base):
    __tablename__ = "detecciones"

    id = Column(Integer, primary_key=True, index=True)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    emocion_detectada = Column(String, nullable=False)
    confianza = Column(Float, nullable=False)
    
    # Timestamp generado automáticamente
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    # Relación de vuelta a la persona
    persona = relationship("Persona", back_populates="detecciones")
