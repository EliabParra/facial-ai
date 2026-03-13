from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool
import json
import logging
from datetime import datetime

from app.database import get_db
from app.utils.image_utils import decode_base64_image
from app.services.emotion_service import clasificar_emocion
from app.services.recognition_service import identificar_persona_en_frame
from app.models.deteccion import Deteccion

router = APIRouter(prefix="/ws", tags=["Reconocimiento Real-Time"])
logger = logging.getLogger(__name__)

@router.websocket("/reconocimiento")
async def websocket_reconocimiento(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    Endpoint WebSocket para recibir frames en tiempo real, analizarlos 
    y devolver la persona identificada y su emoción.
    """
    await websocket.accept()
    logger.info("Cliente WebSocket conectado al streaming facial.")
    
    try:
        while True:
            # Recibir frame comprimido en base64 desde el frontend
            # Esperamos un JSON {"frame": "data:image/jpeg;base64,...."}
            raw_data = await websocket.receive_text()
            
            try:
                payload = json.loads(raw_data)
                frame_b64 = payload.get("frame", "")
                
                if not frame_b64:
                    continue
                
                # Decodificar imagen
                img_array = decode_base64_image(frame_b64)
                
                # Ejecutar el análisis intensivo de IA en un thread pool 
                # para no bloquear el Event Loop asíncrono de FastAPI
                persona, distancia = await run_in_threadpool(
                    identificar_persona_en_frame, img_array, db
                )
                
                # Si reconoció a alguien o si queremos analizar emociones en "desconocidos"
                emocion, confianza_emocion = await run_in_threadpool(
                    clasificar_emocion, img_array
                )
                
                # Preparar respuesta
                response = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "persona": None,
                    "emocion": emocion,
                    "confianza_emocion": round(confianza_emocion, 2),
                    "registrado": False
                }
                
                if persona:
                    response["persona"] = {
                        "id": persona.id,
                        "nombre": persona.nombre,
                        "apellido": persona.apellido
                    }
                    response["registrado"] = True
                    response["distancia_biometrica"] = round(distancia, 4)
                    
                    # Persistir la detección (Opcional: hacer un throttle para no llenar la BD con 30fps)
                    # Aquí lo guardaremos directamente para este MVP, en un caso real se usa batching.
                    nueva_deteccion = Deteccion(
                        persona_id=persona.id,
                        emocion_detectada=emocion,
                        confianza=confianza_emocion,
                        timestamp=datetime.utcnow()
                    )
                    db.add(nueva_deteccion)
                    db.commit()
                
                # Enviar resultados al frontend
                await websocket.send_json(response)
                
            except json.JSONDecodeError:
                logger.warning("Payload WebSocket inválido (no es JSON)")
            except ValueError as e:
                # Fallos comunes de decodificación o IA interna (e.g. no detecta rostro)
                await websocket.send_json({"error": str(e), "registrado": False})
            except Exception as e:
                # Atrapar cualquier otra excepción para no colgar el socket central
                # ej. problemas de OpenCV o de la DB.
                logger.error(f"Error interno en frame: {e}")
                await websocket.send_json({"error": "Error procesando fotograma", "registrado": False})
                
                
    except WebSocketDisconnect:
        logger.info("Cliente WebSocket desconectado.")
    except Exception as e:
        logger.error(f"Error inesperado en WebSocket: {e}")
        try:
            await websocket.close()
        except:
            pass
