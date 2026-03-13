"""
Servicio para clasificación de emociones en tiempo real usando DeepFace.
"""

import numpy as np
from deepface import DeepFace
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def clasificar_emocion(img_array: np.ndarray) -> tuple[str, float]:
    """
    Analiza un rostro en la imagen y retorna la emoción dominante y su porcentaje de confianza.
    """
    try:
        # Enforce detection = False para evitar que el websocket crashee
        # si en un frame rápido no se detecta el rostro completo.
        analysis = DeepFace.analyze(
            img_path=img_array,
            actions=['emotion'],
            enforce_detection=False,
            # Para streaming, opencv es mucho mas rapido que retinaface, 
            # pero dado que el embedding se hizo con retinaface, el crop ideal es el mismo.
            # Sin embargo, para analysis de emocion puro, el detector importa menos, 
            # mantendremos opencv o mtcnn por velocidad en real-time si es necesario.
            # Por consistencia con fase 3, usemos retinaface si hardware lo soporta,
            # o fallback a opencv.
            detector_backend="retinaface" 
        )
        
        if not analysis:
            return "neutral", 0.0
            
        # Tomar la emoción dominante del primer rostro
        dominant_emotion = analysis[0]["dominant_emotion"]
        emotion_score = analysis[0]["emotion"][dominant_emotion]
        
        return dominant_emotion, emotion_score
        
    except Exception as e:
        logger.warning(f"Error detectando emoción: {e}")
        return "neutral", 0.0
