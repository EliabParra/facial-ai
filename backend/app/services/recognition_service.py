"""
Servicio para identificar personas en un frame utilizando sus embeddings guardados.
"""

from typing import Optional
import numpy as np
import json
from sqlalchemy.orm import Session

from app.models.persona import Persona
from app.services.face_service import extraer_embedding, comparar_embeddings
import logging

logger = logging.getLogger(__name__)

def identificar_persona_en_frame(img_array: np.ndarray, db: Session) -> tuple[Optional[Persona], float]:
    """
    Toma un frame, extrae su embedding y lo compara matemáticamente con 
    todos los usuarios registrados en SQLite.
    Retorna la primera Persona que supere el umbral de similitud y su distancia, 
    o (None, 0.0) si no hay coincidencias ("No Registrado").
    """
    try:
        # 1. Extraer embedding del frame actual usando el mismo modelo y backend (RetinaFace)
        frame_embedding = extraer_embedding(img_array)
        
        # 2. Obtener todos los embeddings de la BD
        personas = db.query(Persona).all()
        
        # Búsqueda secuencial (para pocos usuarios). En producción a escala usaríamos pgvector o milvus
        mejor_persona = None
        menor_distancia = float('inf')
        
        for p in personas:
            p_embedding = json.loads(p.embeddings)
            
            # Comparar
            son_iguales, distancia = comparar_embeddings(frame_embedding, p_embedding)
            
            if son_iguales and distancia < menor_distancia:
                menor_distancia = distancia
                mejor_persona = p
                
        return mejor_persona, menor_distancia
        
    except ValueError as e:
        # No se detectó rostro en este frame
        pass
    except Exception as e:
        logger.warning(f"Error identificando rostro en real-time: {e}")
        
    return None, 0.0
