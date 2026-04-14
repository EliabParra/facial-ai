# Facial AI

Este proyecto lo armé para practicar visión por computadora aplicada a algo real: registrar personas, reconocerlas por rostro y además estimar su emoción en tiempo real.

No es solo un demo de cámara. Tiene flujo completo:

- registro de personas (con validaciones)
- detección e identificación en vivo
- análisis de 7 emociones
- historial persistente en base de datos
- reportes con métricas y exportación a CSV

## Qué hace

- Reconocimiento facial usando embeddings con Facenet512 (DeepFace).
- Análisis de emociones: happy, sad, angry, surprise, neutral, fear, disgust.
- Registro con nombre, apellido y email (email único si se carga).
- Captura múltiple de rostro para mejorar calidad de registro.
- Dashboard de reportes por emoción y por persona.
- Exportación de historial a CSV.

## Stack

- Python
- OpenCV
- DeepFace
- CustomTkinter
- SQLAlchemy + SQLite

## Estructura del proyecto

```text
facial-ai/
├── main.py
├── requirements.txt
├── models/
└── src/
    ├── database/
    │   └── db_manager.py
    ├── gui/
    │   ├── app.py
    │   ├── registration_screen.py
    │   ├── detection_screen.py
    │   └── reports_screen.py
    └── logic/
        ├── face_recognizer.py
        └── emotion_analyzer.py
```

## Instalación

Requisitos:

- Python 3.9 o superior
- pip
- Webcam funcional

Pasos:

```bash
# 1) Crear entorno virtual
python -m venv .venv

# 2) Activarlo
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# 3) Instalar dependencias
pip install -r requirements.txt
```

Nota: la primera vez DeepFace descarga los pesos del modelo (Facenet512), así que necesitás internet.

## Ejecutar

```bash
python main.py
```

## Flujo de uso

### 1. Registro

- Completás nombre y apellido (email opcional).
- Hacés varias capturas del rostro.
- El sistema valida calidad (nitidez/tamaño) para evitar registros malos.
- Se guarda el embedding en la base.

### 2. Detección en vivo

- La cámara detecta rostro.
- Se compara contra los embeddings ya guardados.
- Muestra persona identificada + emoción dominante + confianza.
- Cada evento queda logueado.

### 3. Reportes

- Historial de detecciones.
- Métricas generales.
- Gráficos por emoción y por persona.
- Exportación CSV.

## Módulos clave

### src/logic/face_recognizer.py

Se encarga de:

- detectar caras
- generar embeddings
- evaluar calidad de captura
- registrar e identificar personas

### src/logic/emotion_analyzer.py

Se encarga de:

- analizar la cara detectada
- devolver emoción dominante
- devolver score por emoción

### src/database/db_manager.py

Se encarga de:

- CRUD de personas
- almacenamiento de detecciones
- consultas para reportes
- exportación CSV

## Base de datos

Tablas principales:

- persons: datos de persona + embedding serializado.
- detection_logs: eventos de detección con emoción y confianza.

## Estado actual

Es una base sólida para seguir iterando. Ideas que quiero sumar:

- mejorar matching para escenarios con múltiples caras en simultáneo
- filtros avanzados en reportes
- tests automáticos para lógica de reconocimiento

## Contribuciones

Si querés colaborar, mandá PR con cambios claros y bien explicados.

---

Hecho con Python + visión artificial, y muchas horas de prueba/error.
