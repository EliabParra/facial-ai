<template>
  <div class="pointer-events-none absolute inset-0 flex flex-col items-center justify-end pb-8">
    <Transition name="fade">
      <div 
        v-if="result" 
        class="bg-slate-900/80 backdrop-blur-md border border-slate-700 rounded-2xl p-6 shadow-2xl max-w-sm w-full transition-all duration-300 transform"
        :class="result.registrado ? 'border-emerald-500/50 shadow-emerald-500/20' : 'border-rose-500/50 shadow-rose-500/20'"
      >
        <div class="flex items-center space-x-4 mb-4">
          <div 
            class="flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold"
            :class="result.registrado ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'"
          >
            {{ result.registrado ? '✓' : '?' }}
          </div>
          <div>
            <h3 class="text-xl font-bold text-slate-100">
              {{ result.registrado ? `${result.persona.nombre} ${result.persona.apellido}` : 'Desconocido' }}
            </h3>
            <p class="text-sm" :class="result.registrado ? 'text-emerald-400' : 'text-rose-400'">
              {{ result.registrado ? 'Identidad Confirmada' : 'No Registrado' }}
            </p>
          </div>
        </div>
        
        <div v-if="result.error" class="text-rose-400 text-sm font-medium mt-2">
          ⚠️ {{ result.error }}
        </div>
        
        <div v-else class="space-y-3 border-t border-slate-700/50 pt-4">
          <div class="flex justify-between items-center">
            <span class="text-slate-400 text-sm">Emoción Detectada</span>
            <span class="font-medium text-slate-200 capitalize flex items-center gap-2">
              {{ translateEmotion(result.emocion) }}
              <span class="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
                {{ result.confianza_emocion }}%
              </span>
            </span>
          </div>
          
          <div v-if="result.registrado" class="flex justify-between items-center">
            <span class="text-slate-400 text-sm">Distancia Biométrica</span>
            <span class="font-medium text-slate-200 text-sm">
              {{ result.distancia_biometrica }}
            </span>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
defineProps({
  result: {
    type: Object,
    default: null
  }
})

const translateEmotion = (en) => {
  const map = {
    'angry': 'Enojado 😠',
    'disgust': 'Disgusto 🤢',
    'fear': 'Miedo 😨',
    'happy': 'Feliz 😊',
    'sad': 'Triste 😢',
    'surprise': 'Sorpresa 😲',
    'neutral': 'Neutral 😐'
  }
  return map[en?.toLowerCase()] || en
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
