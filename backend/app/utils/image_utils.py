"""
Utilidades para procesamiento de imágenes.
"""

import base64
import numpy as np
import cv2
from fastapi import HTTPException


def decode_base64_image(base64_string: str) -> np.ndarray:
    """
    Decodifica un string base64 en un array de numpy (formato compatible con OpenCV/DeepFace).
    Soporta strings con y sin el prefijo 'data:image/...;base64,'.
    """
    try:
        # Remover prefijo si existe
        if "base64," in base64_string:
            base64_string = base64_string.split("base64,")[1]
            
        # Decodificar
        image_bytes = base64.b64decode(base64_string)
        
        # Convertir a numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decodificar imagen con OpenCV
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("La imagen decodificada está vacía o es corrupta.")
            
        return img
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Error al decodificar la imagen base64: {str(e)}"
        )
