<script setup>
/**
 * ReportesView — Vista de reportes y estadísticas.
 * Placeholder para Fase 1. Se implementará completamente en Fase 5.
 */
</script>

<template>
  <div class="space-y-8">
    <div class="glass-card p-8">
      <div class="flex items-center gap-4 mb-4">
        <div class="flex items-center justify-center w-14 h-14 rounded-2xl bg-yellow-600/20 text-3xl">
          📊
        </div>
        <div>
          <h3 class="text-xl font-bold text-white">Reportes y Estadísticas</h3>
          <p class="text-gray-400 text-sm">Visualiza datos de reconocimiento y tendencias de emociones</p>
        </div>
      </div>
      <div class="border-t border-gray-800/40 pt-6 mt-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Cards placeholder de stats -->
          <div class="flex flex-col items-center justify-center h-40 rounded-xl border-2 border-dashed border-gray-700 bg-gray-800/30">
            <p class="text-3xl mb-2">📈</p>
            <p class="text-gray-400 text-sm font-medium">Gráficos</p>
          </div>
          <div class="flex flex-col items-center justify-center h-40 rounded-xl border-2 border-dashed border-gray-700 bg-gray-800/30">
            <p class="text-3xl mb-2">📋</p>
            <p class="text-gray-400 text-sm font-medium">Historial</p>
          </div>
          <div class="flex flex-col items-center justify-center h-40 rounded-xl border-2 border-dashed border-gray-700 bg-gray-800/30">
            <p class="text-3xl mb-2">⬇️</p>
            <p class="text-gray-400 text-sm font-medium">Exportación</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
