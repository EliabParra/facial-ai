import { ref, onMounted, onUnmounted } from 'vue'

export function useCamera() {
  const videoElement = ref(null)
  const isStreaming = ref(false)
  const stream = ref(null)
  const error = ref(null)

  // Iniciar la cámara solicitando permisos al usuario
  const startCamera = () => {
    return new Promise(async (resolve, reject) => {
      try {
        error.value = null
        stream.value = await navigator.mediaDevices.getUserMedia({ 
          video: { 
            width: { ideal: 1280 }, 
            height: { ideal: 720 },
            facingMode: "user" 
          } 
        })
        
        if (videoElement.value) {
          videoElement.value.srcObject = stream.value
          videoElement.value.onloadedmetadata = () => {
            videoElement.value.play()
            isStreaming.value = true
            resolve(true) // Promesa resuelta solo cuando está 100% reproduciendo
          }
        } else {
          reject(new Error("Elemento de video no encontrado en el DOM"))
        }
      } catch (err) {
        console.error("Error accediendo a la cámara:", err)
        error.value = "No se pudo acceder a la cámara. Verifica los permisos."
        isStreaming.value = false
        reject(err)
      }
    })
  }

  // Detener todos los tracks de la cámara
  const stopCamera = () => {
    if (stream.value) {
      stream.value.getTracks().forEach(track => track.stop())
      stream.value = null
    }
    if (videoElement.value) {
      videoElement.value.srcObject = null
    }
    isStreaming.value = false
  }

  // Capturar frame actual como base64 (JPEG)
  const captureFrame = (quality = 0.8) => {
    if (!isStreaming.value || !videoElement.value) return null
    
    const canvas = document.createElement('canvas')
    canvas.width = videoElement.value.videoWidth
    canvas.height = videoElement.value.videoHeight
    
    const ctx = canvas.getContext('2d')
    ctx.drawImage(videoElement.value, 0, 0, canvas.width, canvas.height)
    
    // Convertir a JPEG base64 (removiendo el prefijo para la API)
    const dataUrl = canvas.toDataURL('image/jpeg', quality)
    return dataUrl.split(',')[1] // Retorna solo el string base64
  }

  // Asegurarse de liberar recursos al destruir el componente
  onUnmounted(() => {
    stopCamera()
  })

  return {
    videoElement,
    isStreaming,
    error,
    startCamera,
    stopCamera,
    captureFrame
  }
}
