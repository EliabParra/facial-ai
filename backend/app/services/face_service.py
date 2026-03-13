"""
Servicio para procesamiento facial usando DeepFace.
Extrae embeddings y calcula similitudes.
"""

import numpy as np
from deepface import DeepFace
from deepface.modules.verification import find_cosine_distance
from fastapi import HTTPException

from app.config import FACE_MODEL, SIMILARITY_THRESHOLD


def extraer_embedding(img_array: np.ndarray) -> list[float]:
    """
    Extrae el vector de características (embedding) de un rostro usando DeepFace.
    """
    try:
        # enforce_detection=True asegura que lance excepción si no encuentra un rostro
        # Retorna una lista de diccionarios (uno por rostro detectado)
        representations = DeepFace.represent(
            img_path=img_array, 
            model_name=FACE_MODEL, 
            enforce_detection=True,
            detector_backend="retinaface"
        )
        
        if not representations:
            raise ValueError("No se obtuvieron representaciones del modelo.")
            
        # Asumimos que la imagen de registro contiene UN SOLO rostro (el principal)
        return representations[0]["embedding"]
        
    except ValueError as e:
        # DeepFace lanza ValueError si no detecta rostros
        if "Face could not be detected" in str(e):
            raise HTTPException(
                status_code=400, 
                detail="No se detectó ningún rostro en la imagen proporcionada. Asegúrate de que el rostro esté visible y bien iluminado."
            )
        raise HTTPException(status_code=500, detail=f"Error en extracción facial: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del motor facial: {str(e)}")


def comparar_embeddings(embedding1: list[float], embedding2: list[float]) -> tuple[bool, float]:
    """
    Compara dos embeddings y devuelve si son la misma persona según el umbral.
    Utiliza distancia Coseno por ser robusta para vectores de alta dimensionalidad.
    Retorna: (son_iguales, distancia)
    """
    # Convertir a listas de list (formato esperado por dst() si no usas numpy direct)
    distancia = find_cosine_distance(embedding1, embedding2)
    
    # Menor distancia = mayor similitud. 
    # Si la distancia <= UMHRAL, son la misma persona.
    son_iguales = distancia <= SIMILARITY_THRESHOLD
    
    return son_iguales, distancia


def promediar_embeddings(lista_embeddings: list[list[float]]) -> list[float]:
    """
    Toma una lista de embeddings obtenidos de múltiples fotos de registro
    y calcula el vector promedio para crear una "firma" más robusta.
    """
    if not lista_embeddings:
        return []
        
    arr = np.array(lista_embeddings)
    mean_embedding = np.mean(arr, axis=0)
    return mean_embedding.tolist()
