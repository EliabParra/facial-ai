# =========================================================
# Backend Dockerfile — FastAPI + DeepFace
# Incluye dependencias de sistema necesarias para OpenCV
# =========================================================
FROM python:3.10-slim

# Dependencias de sistema para OpenCV y DeepFace
# Sin estos paquetes, OpenCV falla al importar libGL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python primero para cachear la capa
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Puerto expuesto por Uvicorn
EXPOSE 8000

# Arrancar con hot-reload para desarrollo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
