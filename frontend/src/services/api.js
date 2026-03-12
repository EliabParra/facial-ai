/**
 * Servicio API — Cliente HTTP para comunicación con el backend.
 *
 * Centraliza todas las peticiones REST al backend de FastAPI.
 * Usa el proxy de Vite en desarrollo (/api → backend:8000).
 */

const API_BASE = '/api'

/**
 * Wrapper genérico para fetch con manejo de errores.
 *
 * @param {string} endpoint - Ruta relativa del endpoint (ej. '/personas')
 * @param {RequestInit} options - Opciones de fetch
 * @returns {Promise<any>} Datos de la respuesta parseados como JSON
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`)
  }

  // Algunos endpoints pueden retornar 204 (No Content)
  if (response.status === 204) return null

  return response.json()
}

/**
 * Health check del backend.
 * @returns {Promise<{status: string, service: string, version: string}>}
 */
export function healthCheck() {
  // El health check está en la raíz, no bajo /api
  return fetch('/').then(r => r.json())
}

export default {
  get: (endpoint) => request(endpoint, { method: 'GET' }),
  post: (endpoint, data) => request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  put: (endpoint, data) => request(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (endpoint) => request(endpoint, { method: 'DELETE' }),
}
