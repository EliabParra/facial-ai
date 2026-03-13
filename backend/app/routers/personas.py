"""
Router para gestión de Personas (Registro y CRUD).
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.persona import Persona
from app.schemas.persona import PersonaCreate, PersonaResponse
from app.utils.image_utils import decode_base64_image
from app.services.face_service import extraer_embedding, comparar_embeddings, promediar_embeddings

router = APIRouter(prefix="/api/personas", tags=["Personas"])


@router.post("/registrar", response_model=PersonaResponse, status_code=status.HTTP_201_CREATED)
def registrar_persona(persona_data: PersonaCreate, db: Session = Depends(get_db)):
    """
    Registra una nueva persona. Recibe datos de texto y una lista de fotos en base64.
    Extrae embeddings de cada foto, calcula el promedio y verifica que no exista
    un rostro similar en la base de datos antes de guardar.
    """
    if not persona_data.fotos:
        raise HTTPException(status_code=400, detail="Se requiere al menos una foto para el registro.")

    # 1. Extraer embeddings de todas las fotos enviadas
    lista_embeddings = []
    for foto_b64 in persona_data.fotos:
        # Decodificar imagen
        img_array = decode_base64_image(foto_b64)
        # Extraer embedding (lanza HTTPException si no hay rostro)
        embedding = extraer_embedding(img_array)
        lista_embeddings.append(embedding)

    # 2. Promediar embeddings para obtener una representación robusta
    embedding_promedio = promediar_embeddings(lista_embeddings)

    # 3. Validar duplicados contra todas las personas en DB
    personas_db = db.query(Persona).all()
    for p_db in personas_db:
        # Deserializar embedding de la DB
        emb_db = json.loads(p_db.embeddings)
        son_iguales, dist = comparar_embeddings(embedding_promedio, emb_db)
        if son_iguales:
            raise HTTPException(
                status_code=409, 
                detail=f"Este rostro ya está registrado a nombre de: {p_db.nombre} {p_db.apellido}."
            )

    # 4. Guardar en base de datos
    nueva_persona = Persona(
        nombre=persona_data.nombre,
        apellido=persona_data.apellido,
        email=persona_data.email,
        embeddings=json.dumps(embedding_promedio) # Guardar como JSON string en SQLite TEXT
    )
    
    try:
        db.add(nueva_persona)
        db.commit()
        db.refresh(nueva_persona)
        return nueva_persona
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El email proporcionado ya está registrado.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar en base de datos: {str(e)}")


@router.get("/", response_model=list[PersonaResponse])
def listar_personas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todas las personas registradas.
    """
    personas = db.query(Persona).offset(skip).limit(limit).all()
    return personas


@router.get("/{persona_id}", response_model=PersonaResponse)
def obtener_persona(persona_id: int, db: Session = Depends(get_db)):
    """
    Devuelve los detalles de una persona específica por ID.
    """
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")
    return persona


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    """
    Elimina una persona y sus históricos de detección (en cascada).
    """
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")
        
    db.delete(persona)
    db.commit()
    return None
