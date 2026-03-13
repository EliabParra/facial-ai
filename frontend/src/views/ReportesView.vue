<template>
  <div class="max-w-5xl mx-auto">
    <header class="mb-8">
      <h1 class="text-3xl font-bold text-slate-100 flex items-center gap-3">
        <span class="text-indigo-500">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </span>
        Panel de Reportes
      </h1>
      <p class="text-slate-400 mt-2">
        Historial de detecciones biométricas y análisis de emociones en tiempo real.
      </p>
    </header>

    <!-- Indicadores Clave (Stats) -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
        <h3 class="text-slate-400 text-sm font-medium">Personas Registradas</h3>
        <p class="text-3xl font-bold text-slate-100 mt-2">
          {{ statLoading ? '...' : stats.total_registrados }}
        </p>
      </div>
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
        <h3 class="text-slate-400 text-sm font-medium">Detecciones Hoy</h3>
        <p class="text-3xl font-bold text-indigo-400 mt-2">
          {{ statLoading ? '...' : stats.detecciones_hoy }}
        </p>
      </div>
      <div class="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg">
        <h3 class="text-slate-400 text-sm font-medium">Emoción del Día</h3>
        <p class="text-3xl font-bold text-emerald-400 mt-2 capitalize flex items-center gap-2">
          {{ statLoading ? '...' : translateEmotion(stats.emocion_predominante_hoy) }}
        </p>
      </div>
    </div>

    <!-- Tabla de Historial Reciente -->
    <div class="bg-slate-800 border border-slate-700 rounded-xl shadow-xl overflow-hidden">
      <div class="p-6 border-b border-slate-700 flex justify-between items-center">
        <h2 class="text-lg font-bold text-slate-200">Últimos Avistamientos</h2>
        <button 
          @click="fetchData" 
          class="text-indigo-400 hover:text-indigo-300 text-sm flex items-center gap-1 transition-colors"
          :class="{ 'opacity-50 pointer-events-none': listLoading }"
        >
          <svg class="w-4 h-4" :class="{ 'animate-spin': listLoading }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Actualizar
        </button>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-300">
          <thead class="text-xs text-slate-400 uppercase bg-slate-900/50">
            <tr>
              <th scope="col" class="px-6 py-4">Fecha y Hora</th>
              <th scope="col" class="px-6 py-4">Identidad</th>
              <th scope="col" class="px-6 py-4">Emoción (DeepFace)</th>
              <th scope="col" class="px-6 py-4">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="detecciones.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-slate-500">
                Aún no hay detecciones en el sistema para mostrar.
              </td>
            </tr>
            <tr 
              v-else
              v-for="det in detecciones" 
              :key="det.id"
              class="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                {{ formatDateTime(det.timestamp) }}
              </td>
              <td class="px-6 py-4 font-medium" :class="det.persona.nombre === 'Desconocido' ? 'text-slate-500' : 'text-slate-200'">
                {{ det.persona.nombre }} {{ det.persona.apellido }}
              </td>
              <td class="px-6 py-4 capitalize">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-slate-900 border border-slate-700">
                  {{ getEmotionEmoji(det.emocion) }} {{ translateEmotion(det.emocion) }}
                  <span class="text-slate-500 text-[10px] ml-1">{{ Math.round(det.confianza) }}%</span>
                </span>
              </td>
              <td class="px-6 py-4">
                <span v-if="det.persona.nombre !== 'Desconocido'" class="inline-flex items-center gap-1.5 text-emerald-400 text-xs font-medium">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Identidad Confirmada
                </span>
                <span v-else class="inline-flex items-center gap-1.5 text-rose-400 text-xs font-medium">
                  <span class="w-2 h-2 rounded-full bg-rose-500"></span> Desconocido
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const stats = ref({
  total_registrados: 0,
  detecciones_hoy: 0,
  emocion_predominante_hoy: 'Ninguna'
})
const detecciones = ref([])
const statLoading = ref(true)
const listLoading = ref(true)

const fetchData = async () => {
  try {
    statLoading.value = true
    listLoading.value = true
    
    // Obteniendo estadisticas
    const statRes = await fetch('/api/reportes/estadisticas')
    if (statRes.ok) stats.value = await statRes.json()
    
    // Obteniendo historial
    const detRes = await fetch('/api/reportes/detecciones')
    if (detRes.ok) detecciones.value = await detRes.json()
    
  } catch (error) {
    console.error("Error cargando reportes:", error)
  } finally {
    statLoading.value = false
    listLoading.value = false
  }
}

onMounted(() => {
  fetchData()
})

const formatDateTime = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return new Intl.DateTimeFormat('es-ES', {
    day: 'numeric', month: 'short', 
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  }).format(date)
}

const translateEmotion = (en) => {
  const map = {
    angry: 'enojado', disgust: 'disgustado', fear: 'miedo',
    happy: 'feliz', sad: 'triste', surprise: 'sorpresa', neutral: 'neutral',
    Ninguna: 'Sin Datos'
  }
  return map[en?.toLowerCase()] || en
}

const getEmotionEmoji = (en) => {
  const map = {
    angry: '😠', disgust: '🤢', fear: '😨',
    happy: '😊', sad: '😢', surprise: '😲', neutral: '😐'
  }
  return map[en?.toLowerCase()] || '❓'
}
</script>
