# 1. Stack Detectado
* **Infraestructura:** Docker, Docker Compose.
* **Backend:** Python 3.10, FastAPI, OpenCV, DeepFace, SQLAlchemy, Uvicorn, WebSockets.
* **Frontend:** Node.js, Vite 5, Vue 3 (Composition API `<script setup>`), Tailwind CSS, Chart.js / vue-chartjs.
* **Base de Datos:** SQLite, Adminer.

# 2. Reglas de Estilo (Linter/Format)
* **Python:** Cumplimiento estricto de PEP8. Usar type hints en todas las funciones de FastAPI.
* **Vue:** Usar Composition API de forma exclusiva. Componentes modulares y con alcance (scoped CSS o Tailwind utility classes).
* [cite_start]**Buenas Prácticas:** Código organizado modularmente [cite: 55] [cite_start]y con manejo de errores robusto[cite: 56].

# 3. Definiciones de Datos
* **Tabla `Personas`:** * `id` (PK)
    * [cite_start]`nombre` (String) [cite: 8]
    * [cite_start]`apellido` (String) [cite: 8]
    * [cite_start]`email` (String, Unique) [cite: 8]
    * [cite_start]`embeddings` (Blob/Text - JSON serializado de DeepFace) [cite: 7]
* **Tabla `Detecciones`:** * `id` (PK)
    * `persona_id` (FK -> Personas)
    * [cite_start]`emocion_detectada` (String) [cite: 42]
    * [cite_start]`confianza` (Float) [cite: 43]
    * [cite_start]`timestamp` (DateTime) [cite: 44]