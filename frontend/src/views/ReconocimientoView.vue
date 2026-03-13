<template>
  <div class="max-w-5xl mx-auto">
    <header class="mb-8">
      <h1 class="text-3xl font-bold text-slate-100 flex items-center gap-3">
        <span class="text-indigo-500">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
        </span>
        Reconocimiento en Tiempo Real
      </h1>
      <p class="text-slate-400 mt-2">
        El sistema enviará fotogramas comprimidos al motor de inteligencia artificial vía WebSocket.
      </p>
    </header>

    <div class="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden shadow-xl p-6">
      <!-- Controles Superiores -->
      <div class="flex justify-between items-center mb-6">
        <div class="flex items-center space-x-4">
          <div class="w-3 h-3 rounded-full" :class="isConnected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'"></div>
          <span class="text-sm font-medium" :class="isConnected ? 'text-emerald-400' : 'text-rose-400'">
            {{ isConnected ? 'Servidor IA Conectado' : 'Desconectado del Servidor' }}
          </span>
        </div>
        
        <div class="flex gap-4">
          <button 
            v-if="!isStreaming"
            @click="empezarReconocimiento" 
            class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl transition-colors shadow-lg shadow-indigo-500/20"
          >
            Activar Sistema
          </button>
          <button 
            v-else
            @click="detenerReconocimiento" 
            class="px-6 py-2.5 bg-rose-500 hover:bg-rose-600 text-white font-medium rounded-xl transition-colors shadow-lg shadow-rose-500/20"
          >
            Detener Transmisión
          </button>
        </div>
      </div>

      <!-- Area de Video Principal -->
      <div class="relative bg-slate-900 rounded-xl overflow-hidden aspect-video border border-slate-700/50 shadow-inner flex items-center justify-center">
        <!-- Error Camera -->
        <div v-if="cameraError" class="absolute inset-0 flex flex-col items-center justify-center p-8 text-center z-10">
          <div class="w-16 h-16 bg-rose-500/20 rounded-full flex items-center justify-center mb-4">
            <svg class="w-8 h-8 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <p class="text-rose-400">{{ cameraError }}</p>
        </div>
        
        <!-- Estado Inicial -->
        <div v-if="!isStreaming && !cameraError" class="absolute inset-0 flex flex-col items-center justify-center text-slate-500 text-center z-10 p-8">
          <svg class="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <p>Presiona "Activar Sistema" para iniciar la lectura biométrica a través de la webcam.</p>
        </div>

        <!-- Elemento de Video Real -->
        <video 
          ref="videoElement"
          class="w-full h-full object-cover transition-opacity duration-700"
          :class="{ 'opacity-0': !isStreaming, 'opacity-100': isStreaming }"
          autoplay 
          playsinline
          muted
          style="transform: scaleX(-1);"
        ></video>

        <!-- Overlay de IA (Solo si está stremeando) -->
        <FaceOverlay v-if="isStreaming" :result="lastResult" />
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { useCamera } from '../composables/useCamera'
import { useWebSocket } from '../composables/useWebSocket'
import FaceOverlay from '../components/FaceOverlay.vue'

// Determinar el host correcto basada en el proxy de vite
// Si el frontend corre en el puerto 5173 e inyecta proxy, Vite rutea WS
// Sin embargo, WebSocket directo es mas seguro en puertos absolutos usando window.location
// En Vite proxy: ws://localhost:5173/ws/reconocimiento 
const wsUrl = window.location.protocol === 'https:' 
  ? `wss://${window.location.host}/ws/reconocimiento`
  : `ws://${window.location.host}/ws/reconocimiento`

const { videoElement, isStreaming, error: cameraError, startCamera, stopCamera, captureFrame } = useCamera()
const { isConnected, lastResult, sendFrame } = useWebSocket(wsUrl)

let transmisionActiva = false
let framesEnviados = 0

const bucleFotogramas = async () => {
  // Solo destruir el bucle si el usuario hace clic en "Detener Transmisión"
  if (!transmisionActiva) {
    console.log("[WS] Bucle detenido por transmisionActiva=false");
    return;
  }
  
  // Si la cámara sirve y el WS está en verde, procesamos la foto
  if (isStreaming.value && isConnected.value) {
    console.log("[WS] Intentando capturar frame...");
    const frameBase64 = captureFrame(0.6)
    
    if (frameBase64) {
      console.log(`[WS] Enviando Frame #${framesEnviados} (${Math.round(frameBase64.length / 1024)} KB)`);
      sendFrame(frameBase64)
      framesEnviados++
    } else {
      console.warn("[WS] CaptureFrame devolvió un frame vacío o nulo.");
    }
  } else {
    console.warn(`[WS] Bucle saltado: isStreaming=${isStreaming.value}, isConnected=${isConnected.value}`);
  }

  // Y sin importar si mandó o no, agendamos la próxima verificación
  setTimeout(bucleFotogramas, 800)
}

const empezarReconocimiento = async () => {
  console.log("[UI] Botón Activar Sistema presionado.");
  await startCamera()
  
  if (isStreaming.value) {
    console.log("[UI] Cámara iniciada correctamente. Activando Transmision...");
    transmisionActiva = true
    framesEnviados = 0
    // Lanzar el ciclo asíncrono
    bucleFotogramas()
  } else {
    console.error("[UI] La cámara no pudo reportar isStreaming=true tras startCamera().");
  }
}

const detenerReconocimiento = () => {
  transmisionActiva = false
  stopCamera()
}

// Limpiar al desmontar
onUnmounted(() => {
  detenerReconocimiento()
})

</script>
