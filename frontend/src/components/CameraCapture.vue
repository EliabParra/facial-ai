<script setup>
import { onMounted, watch } from 'vue'
import { useCamera } from '../composables/useCamera.js'

const props = defineProps({
  // Indica si la cámara debe arrancar automáticamente
  autoStart: { type: Boolean, default: false }
})

const emit = defineEmits(['capture', 'error'])

const { 
  videoElement, 
  isStreaming, 
  error, 
  startCamera, 
  stopCamera, 
  captureFrame 
} = useCamera()

// Emitir errores hacia el componente padre
watch(error, (newError) => {
  if (newError) emit('error', newError)
})

onMounted(() => {
  if (props.autoStart) {
    startCamera()
  }
})

// Función expuesta o utilizada internamente para capturar
const takePhoto = () => {
  const base64 = captureFrame(0.9) // Alta calidad para registro
  if (base64) {
    emit('capture', base64)
  }
}

// Exponer métodos para que el padre pueda controlarla
defineExpose({
  startCamera,
  stopCamera,
  takePhoto,
  isStreaming
})
</script>

<template>
  <div class="relative w-full rounded-2xl overflow-hidden bg-gray-900 border border-gray-700/50 shadow-inner group">
    <!-- Overlay de carga / error -->
    <div v-if="!isStreaming" class="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-10 bg-gray-900/80 backdrop-blur-sm">
      <div v-if="error" class="text-red-400">
        <svg class="w-10 h-10 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        <p class="font-medium mb-4">{{ error }}</p>
        <button @click="startCamera" class="btn-secondary text-sm">Reintentar</button>
      </div>
      <div v-else class="text-gray-400">
        <svg class="w-10 h-10 mx-auto mb-3 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
        <p class="font-medium animate-pulse">Iniciando cámara...</p>
      </div>
    </div>
    
    <!-- Elemento Video -->
    <!-- object-cover y scale-x-[-1] para efecto espejo -->
    <video 
      ref="videoElement" 
      autoplay 
      playsinline 
      muted
      class="w-full h-full min-h-[320px] object-cover scale-x-[-1]"
    ></video>
    
    <!-- UI Superpuesta (Frame delimitador para rostro) -->
    <div v-if="isStreaming" class="absolute inset-0 pointer-events-none">
      <!-- Borde para guiar al usuario -->
      <div class="w-full h-full flex items-center justify-center p-8">
        <div class="w-56 h-72 border-2 border-primary-500/50 border-dashed rounded-[3rem] transition-all duration-300 shadow-[0_0_0_9999px_rgba(17,24,39,0.4)]"></div>
      </div>
      
      <!-- Botones de control flotantes (opcional, pueden estar en el padre) -->
      <div class="absolute bottom-4 left-0 right-0 flex justify-center pb-2 pointer-events-auto opacity-0 group-hover:opacity-100 transition-opacity">
        <button @click="takePhoto" type="button" class="w-14 h-14 bg-white rounded-full flex items-center justify-center hover:bg-gray-200 active:scale-95 transition-all shadow-lg ring-4 ring-white/20">
          <div class="w-11 h-11 border-2 border-gray-400 rounded-full"></div>
        </button>
      </div>
    </div>
  </div>
</template>
