# 1. Objetivo del proyecto
[cite_start]Construir un Sistema de Reconocimiento Facial con Análisis de Emociones[cite: 2]. [cite_start]El sistema debe permitir el registro de individuos, la extracción de embeddings faciales [cite: 7][cite_start], y la detección de emociones en tiempo real [cite: 11] a través de una arquitectura web contenerizada de 3 capas.

# 2. Análisis Crítico del Estado Actual
* **Riesgo de Rendimiento (WebSockets):** Transmitir video en vivo frame por frame hacia el backend puede generar alta latencia. Se requerirá compresión de frames en el frontend (Vue) antes de enviarlos por el socket.
* **Riesgo de Concurrencia (SQLite):** SQLite es excelente para desarrollo, pero tiene limitaciones con escrituras concurrentes. Se debe configurar SQLAlchemy con `check_same_thread=False` y manejar correctamente las sesiones de base de datos en FastAPI.
* **Dependencias Pesadas:** OpenCV y DeepFace requieren binarios del sistema (ej. `libgl1-mesa-glx`). El `Dockerfile` del backend debe incluir estos paquetes a nivel de sistema operativo para evitar fallos de compilación.

# 3. Plan de Arquitectura
Se implementará una arquitectura basada en microservicios mediante Docker Compose:
* **Frontend (Vue 3 + Vite):** Actuará como cliente pesado. Capturará el flujo de la cámara, renderizará la UI estática (Tailwind) y mostrará overlays reactivos.
* [cite_start]**Backend (FastAPI + DeepFace):** Proveerá una API REST para el CRUD de usuarios y reportes, y un canal WebSocket para el procesamiento de IA en tiempo real (extracción de embeddings y clasificación de 7 emociones [cite: 14]).
* **Persistencia:** Volumen local mapeado a SQLite, accesible vía Adminer para inspección y debugging.