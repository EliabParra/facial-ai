import { ref, onMounted, onUnmounted } from 'vue'

export function useWebSocket(url) {
  const ws = ref(null)
  const isConnected = ref(false)
  const lastResult = ref(null)
  const error = ref(null)
  
  let reconnectTimer = null

  const connect = () => {
    try {
      ws.value = new WebSocket(url)
      
      ws.value.onopen = () => {
        isConnected.value = true
        error.value = null
        console.log('WebSocket conectado a', url)
      }
      
      ws.value.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          lastResult.value = data
        } catch (e) {
          console.error("Error parseando mensaje WS:", e)
        }
      }
      
      ws.value.onerror = (e) => {
        console.error('Error en WebSocket:', e)
        error.value = 'Error de conexión con el motor de IA.'
      }
      
      ws.value.onclose = () => {
        if (isConnected.value) {
          console.log('WebSocket desconectado. Intentando reconectar...')
          isConnected.value = false
          // Auto-reconnect
          reconnectTimer = setTimeout(connect, 3000)
        }
      }
    } catch (e) {
      error.value = 'Failed to create WebSocket.'
      console.error(e)
    }
  }

  const sendFrame = (frameBase64) => {
    if (ws.value && ws.value.readyState === WebSocket.OPEN) {
      ws.value.send(JSON.stringify({ frame: frameBase64 }))
    }
  }

  const disconnect = () => {
    if (reconnectTimer) clearTimeout(reconnectTimer)
    if (ws.value) {
      // Evitar que onclose intente reconectar si cerramos intencionalmente
      ws.value.onclose = null 
      ws.value.close()
      isConnected.value = false
    }
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    isConnected,
    lastResult,
    error,
    sendFrame,
    disconnect,
    connect
  }
}
