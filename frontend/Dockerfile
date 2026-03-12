# =========================================================
# Frontend Dockerfile — Vue 3 + Vite
# Servidor de desarrollo con hot-reload
# =========================================================
FROM node:20-alpine

WORKDIR /app

# Instalar dependencias primero para cachear la capa
COPY package.json package-lock.json* ./
RUN npm install

# Copiar código fuente
COPY . .

# Puerto expuesto por Vite
EXPOSE 5173

# Arrancar servidor de desarrollo accesible desde fuera del contenedor
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
