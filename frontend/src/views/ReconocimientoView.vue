<script setup>
/**
 * ReconocimientoView — Vista de reconocimiento facial en tiempo real.
 * Placeholder para Fase 1. Se implementará completamente en Fase 4.
 */
</script>

<template>
  <div class="space-y-8">
    <div class="glass-card p-8">
      <div class="flex items-center gap-4 mb-4">
        <div class="flex items-center justify-center w-14 h-14 rounded-2xl bg-accent-600/20 text-3xl">
          🎯
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Reconocimiento en Tiempo Real</h3>
          <p class="text-gray-400 text-sm">Identifica personas y analiza emociones con la cámara en vivo</p>
        </div>
      </div>
      <div class="border-t border-gray-800/40 pt-6 mt-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Preview de cámara -->
          <div class="flex items-center justify-center h-72 rounded-xl border-2 border-dashed border-gray-700 bg-gray-800/30">
            <div class="text-center">
              <p class="text-4xl mb-3">📹</p>
              <p class="text-gray-400 font-medium">Streaming de Video</p>
              <p class="text-gray-600 text-sm mt-1">Fase 4</p>
            </div>
          </div>
          <!-- Panel de información -->
          <div class="flex items-center justify-center h-72 rounded-xl border-2 border-dashed border-gray-700 bg-gray-800/30">
            <div class="text-center">
              <p class="text-4xl mb-3">😊</p>
              <p class="text-gray-400 font-medium">Panel de Emociones</p>
              <p class="text-gray-600 text-sm mt-1">Fase 4</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
