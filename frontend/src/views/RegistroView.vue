<script setup>
import { ref, computed } from 'vue'
import CameraCapture from '../components/CameraCapture.vue'
import api from '../services/api.js'

// Estado del formulario
const form = ref({
  nombre: '',
  apellido: '',
  email: ''
})

// Estado de la captura
const cameraRef = ref(null)
const fotos = ref([])
const isCapturing = ref(false)
const maxFotos = 3

// Estado de la UI
const loading = ref(false)
const errorMsg = ref(null)
const successMsg = ref(null)

// Validaciones
const isValidForm = computed(() => {
  return form.value.nombre.trim() !== '' && 
         form.value.apellido.trim() !== '' && 
         form.value.email.includes('@') &&
         fotos.value.length > 0
})

const fotosFaltantes = computed(() => maxFotos - fotos.value.length)

// Manejo de eventos de cámara
const handleCapture = (base64Img) => {
  if (fotos.value.length < maxFotos) {
    fotos.value.push(base64Img)
  }
}

const handleCameraError = (err) => {
  errorMsg.value = err
}

const toggleCamera = () => {
  if (cameraRef.value?.isStreaming) {
    cameraRef.value.stopCamera()
    isCapturing.value = false
  } else {
    errorMsg.value = null
    successMsg.value = null
    cameraRef.value?.startCamera()
    isCapturing.value = true
  }
}

const removeFoto = (index) => {
  fotos.value.splice(index, 1)
}

// Envío al backend
const registrarPersona = async () => {
  if (!isValidForm.value) return
  
  loading.value = true
  errorMsg.value = null
  successMsg.value = null
  
  try {
    const payload = {
      ...form.value,
      fotos: fotos.value
    }
    
    await api.post('/personas/registrar', payload)
    
    // Éxito
    successMsg.value = `¡${form.value.nombre} registrado correctamente en el sistema!`
    
    // Limpiar formulario interactivo
    if (cameraRef.value?.isStreaming) {
      cameraRef.value.stopCamera()
    }
    isCapturing.value = false
    fotos.value = []
    form.value = { nombre: '', apellido: '', email: '' }
    
  } catch (err) {
    errorMsg.value = err.message || "Error al conectar con el servidor"
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="space-y-6 max-w-6xl mx-auto">
    <!-- Hero Section / Header -->
    <div class="glass-card p-6 md:p-8">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <div class="flex items-center justify-center w-14 h-14 rounded-2xl bg-primary-600/20 text-3xl">
            👤
          </div>
          <div>
            <h3 class="text-xl md:text-2xl font-bold text-white">Registro de Personas</h3>
            <p class="text-gray-400 text-sm mt-1">Registra nuevos individuos capturando sus rasgos faciales</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Alertas globales -->
    <div v-if="errorMsg" class="p-4 rounded-xl bg-red-900/30 border border-red-800 text-red-300 flex items-start gap-3">
      <span class="mt-0.5">⚠️</span>
      <p class="text-sm font-medium">{{ errorMsg }}</p>
    </div>
    <div v-if="successMsg" class="p-4 rounded-xl bg-accent-900/30 border border-accent-800 text-accent-300 flex items-start gap-3">
      <span class="mt-0.5">✅</span>
      <p class="text-sm font-medium">{{ successMsg }}</p>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      
      <!-- Panel Izquierdo: Formulario (5 columnas) -->
      <div class="glass-card p-6 lg:col-span-5 h-fit">
        <h4 class="text-lg font-semibold text-white mb-5 border-b border-gray-800 pb-3">Datos Personales</h4>
        
        <form @submit.prevent="registrarPersona" class="space-y-4">
          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-400">Nombre</label>
            <input 
              v-model="form.nombre" 
              type="text" 
              required
              placeholder="Ej. Juan"
              class="w-full bg-gray-900/50 border border-gray-700 rounded-xl px-4 py-2.5 text-white placeholder-gray-600 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-colors"
              :disabled="loading"
            >
          </div>
          
          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-400">Apellido</label>
            <input 
              v-model="form.apellido" 
              type="text" 
              required
              placeholder="Ej. Pérez"
              class="w-full bg-gray-900/50 border border-gray-700 rounded-xl px-4 py-2.5 text-white placeholder-gray-600 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-colors"
              :disabled="loading"
            >
          </div>
          
          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-400">Correo Electrónico</label>
            <input 
              v-model="form.email" 
              type="email" 
              required
              placeholder="juan.perez@email.com"
              class="w-full bg-gray-900/50 border border-gray-700 rounded-xl px-4 py-2.5 text-white placeholder-gray-600 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-colors"
              :disabled="loading"
            >
          </div>

          <div class="pt-6 mt-4 border-t border-gray-800">
            <button 
              type="submit" 
              class="btn-primary w-full py-3 flex items-center justify-center gap-2"
              :disabled="!isValidForm || loading"
              :class="{ 'opacity-50 cursor-not-allowed': !isValidForm || loading }"
            >
              <span v-if="loading" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              <span v-else>Guardar Persona</span>
            </button>
            <p v-if="!isValidForm && !loading" class="text-xs text-center text-gray-500 mt-3">
              Completa los datos y toma al menos 1 foto.
            </p>
          </div>
        </form>
      </div>

      <!-- Panel Derecho: Cámara (7 columnas) -->
      <div class="glass-card p-6 lg:col-span-7 flex flex-col">
        <div class="flex items-center justify-between mb-5 border-b border-gray-800 pb-3">
          <h4 class="text-lg font-semibold text-white">Captura Facial</h4>
          <span class="status-badge" :class="fotos.length > 0 ? 'bg-accent-500/20 text-accent-400' : 'bg-yellow-500/20 text-yellow-500'">
            {{ fotos.length }} / {{ maxFotos }} Fotos
          </span>
        </div>

        <!-- Layout dinámico dependiendo si la cámara está activa o no -->
        <div class="relative flex-1 flex flex-col min-h-[400px]">
          
          <!-- Componente de Cámara (Visible solo si está capturando) -->
          <div v-show="isCapturing" class="flex-1 w-full rounded-2xl overflow-hidden shadow-2xl bg-black max-h-[450px]">
            <CameraCapture 
              ref="cameraRef"
              @capture="handleCapture"
              @error="handleCameraError"
            />
            
            <!-- Botón interno para tomar foto si no usamos el hover del componente base -->
            <div class="absolute inset-x-0 bottom-6 flex justify-center pb-safe">
              <button 
                @click="cameraRef?.takePhoto()"
                class="w-16 h-16 bg-white/20 backdrop-blur-md rounded-full flex items-center justify-center hover:bg-white/30 active:scale-95 transition-all shadow-xl border border-white/40 group z-20"
                :disabled="fotos.length >= maxFotos"
              >
                <div class="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg group-active:w-10 group-active:h-10 transition-all">
                  📸
                </div>
              </button>
            </div>
          </div>
          
          <!-- Estado inactivo (No capturando fotos) -->
          <div v-show="!isCapturing && fotos.length === 0" class="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-gray-700 rounded-2xl bg-gray-900/30">
            <div class="w-20 h-20 rounded-full bg-gray-800 flex items-center justify-center text-4xl mb-4">
              📷
            </div>
            <p class="text-gray-400 font-medium mb-1">Cámara Inactiva</p>
            <p class="text-gray-500 text-sm text-center max-w-xs mb-6">Activa la cámara para registrar el rostro de esta persona. Se recomiendan {{ maxFotos }} fotos de distintos ángulos.</p>
            
            <button @click="toggleCamera" type="button" class="btn-primary">
              Iniciar Cámara
            </button>
          </div>

          <!-- Galería de fotos capturadas -->
          <div v-if="!isCapturing && fotos.length > 0" class="flex-1">
            <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div 
                v-for="(foto, index) in fotos" 
                :key="index"
                class="relative aspect-[3/4] rounded-xl overflow-hidden border border-gray-700 bg-gray-900 group"
              >
                <!-- Renderiza el base64 sin el prefijo que quitamos en captureFrame -->
                <img :src="`data:image/jpeg;base64,${foto}`" class="w-full h-full object-cover scale-x-[-1]" />
                
                <!-- Botón borrar -->
                <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="removeFoto(index)" class="flex items-center justify-center w-7 h-7 bg-red-500 hover:bg-red-600 outline outline-[3px] outline-gray-900 text-white rounded-full">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                  </button>
                </div>
              </div>
              
              <!-- Placeholder añadir más -->
              <div 
                v-if="fotosFaltantes > 0"
                @click="toggleCamera"
                class="aspect-[3/4] rounded-xl border-2 border-dashed border-gray-700 bg-gray-800/30 flex flex-col items-center justify-center cursor-pointer hover:bg-gray-800/50 hover:border-gray-500 transition-colors"
              >
                <div class="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center text-white mb-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                </div>
                <span class="text-xs font-medium text-gray-400 text-center px-2">Añadir otra foto <br> ({{ fotosFaltantes }} restantes)</span>
              </div>
            </div>
          </div>
          
        </div>
        
        <!-- Controles inferiores de cámara -->
        <div class="mt-4 flex justify-end">
           <button 
             v-if="isCapturing"
             @click="toggleCamera" 
             type="button" 
             class="btn-secondary text-sm"
           >
             Cerrar Cámara
           </button>
        </div>
        
      </div>
      
    </div>
  </div>
</template>

<style scoped>
.pb-safe {
  padding-bottom: max(1.5rem, env(safe-area-inset-bottom));
}
</style>
