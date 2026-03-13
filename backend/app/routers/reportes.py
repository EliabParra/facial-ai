from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta

from app.database import get_db
from app.models.persona import Persona
from app.models.deteccion import Deteccion

router = APIRouter(prefix="/api/reportes", tags=["Reportes"])

@router.get("/detecciones")
def obtener_ultimas_detecciones(db: Session = Depends(get_db), limit: int = 50):
    """
    Retorna el historial de las últimas detecciones ordenadas por la más reciente.
    Incluye los datos básicos de la persona detectada.
    """
    detecciones = db.query(Deteccion).order_by(desc(Deteccion.timestamp)).limit(limit).all()
    
    resultados = []
    for d in detecciones:
        persona = db.query(Persona).filter(Persona.id == d.persona_id).first()
        resultados.append({
            "id": d.id,
            "timestamp": d.timestamp.isoformat() + "Z",
            "emocion": d.emocion_detectada,
            "confianza": d.confianza,
            "persona": {
                "nombre": persona.nombre if persona else "Desconocido",
                "apellido": persona.apellido if persona else ""
            }
        })
        
    return resultados

@router.get("/estadisticas")
def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    """
    Retorna métricas clave para el dashboard:
    - Total de personas registradas
    - Total de detecciones hoy
    - Emoción más frecuente del día
    """
    hoy = datetime.utcnow().date()
    inicio_dia = datetime(hoy.year, hoy.month, hoy.day)
    
    total_personas = db.query(Persona).count()
    
    # Detecciones de hoy
    detecciones_hoy = db.query(Deteccion).filter(Deteccion.timestamp >= inicio_dia).all()
    total_detecciones_hoy = len(detecciones_hoy)
    
    # Calcular emoción más frecuente
    conteo_emociones = {}
    for d in detecciones_hoy:
        conteo_emociones[d.emocion_detectada] = conteo_emociones.get(d.emocion_detectada, 0) + 1
        
    emocion_frecuente = "Ninguna"
    if conteo_emociones:
        emocion_frecuente = max(conteo_emociones, key=conteo_emociones.get)
        
    return {
        "total_registrados": total_personas,
        "detecciones_hoy": total_detecciones_hoy,
        "emocion_predominante_hoy": emocion_frecuente
    }
