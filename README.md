# Facial-AI: Reconocimiento Facial en Tiempo Real con Análisis de Emociones

Sistema web contenerizado de 3 capas diseñado para registrar individuos, extraer sus embeddings faciales mediante Inteligencia Artificial profunda (DeepFace + RetinaFace) y clasificar sus perfiles emocionales en tiempo real a través de transmisiones por WebSocket.

![Status](https://img.shields.io/badge/Status-Completado-success)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Vue](https://img.shields.io/badge/Vue-3.x-4fc08d)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ed)

## 📋 Características Principales

1. **Gestión Bio-Métrica:** Módulo de registro de personas que captura múltiples fotografías con validación de calidad.
2. **Motor DeepFace:** Inferencia local mediante TensorFlow para codificación facial en un vector multidimensional, detectando falsos positivos y duplicidades.
3. **Stream WebSocket 24/7:** Frontend robusto en Vue 3 que captura fotogramas de la webcam mediante una recursividad asincrónica ininterrumpida y resistente a fallos de red.
4. **Análisis de Emociones:** Clasificación del espectro emocional (Feliz, Triste, Enojado, Sorprendido, Temeroso, Disgustado, Neutral).
5. **Dashboard Analítico:** Panel de reportes estadísticos alimentado de los metadatos SQL guardados por el sistema de detección.

## 🏗 Arquitectura del Sistema

* **Frontend:** Vue 3 (Composition API) + Vite + TailwindCSS v3.
* **Backend:** FastAPI (Python asíncrono) + OpenCV (headless) + DeepFace/TensorFlow.
* **Database:** SQLite3 incrustado manejado mediante SQLAlchemy ORM (modo WAL concurrente).
* **Infraestructura:** Despliegue de orquestación `docker-compose` en 3 contenedores separados (Frontend, Backend, Adminer).

## 🚀 Guía de Instalación y Despliegue

### Prerrequisitos
- Docker Engine & Docker Compose instalados.
- Cámara Web conectada y disponible en el equipo Host.

### Levantar el Ecosistema

1. Clona el repositorio y navega a la carpeta principal:
```bash
git clone <url-repo> facial-ai
cd facial-ai
```

2. Ejecuta el constructor de contenedores (esto descargará los pesos de TensorFlow y Node.js):
```bash
docker compose up --build -d
```

3. El sistema estará disponible en los siguientes puertos:
- **Frontend SPA:** [http://localhost:5173](http://localhost:5173)
- **FastAPI / Swagger UI:** [http://localhost:8001/docs](http://localhost:8001/docs)
- **Base de Datos DbAdmin:** [http://localhost:8080](http://localhost:8080)

## 🔧 Resoluciones Técnicas Relevantes

* **Resiliencia de Streaming:** El ciclo original `setInterval` de Vue 3 fue reemplazado por un patrón de Promesas recursivas (`setTimeout`) sobre `video.onloadedmetadata` garantizando inicializaciones impecables dictadas por hardware.
* **Tolerancia a Fallos Internos:** FastAPI se envolvió en barreras `try-except Exception` críticas dentro del bucle de Websocket para impedir caídas de Uvicorn si DeepFace falla al localizar un rostro en fotogramas oscuros o corruptos.

## 👨‍💻 Autor
Construido por Antigravity AI (Pair Programming Arquitectónico con el Dev Principal).
Licencia: MIT.
