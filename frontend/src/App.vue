<script setup>
/**
 * App.vue — Layout principal de la aplicación.
 *
 * Contiene la navegación lateral fija y el área de contenido
 * con transiciones entre vistas.
 */
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { routes } from './router/index.js'

const route = useRoute()
const router = useRouter()
const isSidebarCollapsed = ref(false)

const currentTitle = computed(() => route.meta?.title || 'Facial-AI')

function toggleSidebar() {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <!-- ===== Sidebar ===== -->
    <aside
      :class="[
        'flex flex-col border-r border-gray-800/60 bg-gray-900/80 backdrop-blur-xl transition-all duration-300',
        isSidebarCollapsed ? 'w-20' : 'w-64'
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-5 py-6 border-b border-gray-800/40">
        <div class="flex items-center justify-center w-10 h-10 rounded-xl bg-primary-600 text-white font-bold text-lg shadow-lg shadow-primary-600/30">
          FA
        </div>
        <transition name="fade">
          <div v-if="!isSidebarCollapsed" class="overflow-hidden">
            <h1 class="text-lg font-bold text-white leading-tight">Facial-AI</h1>
            <p class="text-xs text-gray-500">Reconocimiento Facial</p>
          </div>
        </transition>
      </div>

      <!-- Navegación -->
      <nav class="flex-1 px-3 py-4 space-y-1">
        <router-link
          v-for="r in routes"
          :key="r.name"
          :to="r.path"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-200 group',
            route.name === r.name 
              ? 'bg-primary-600/20 text-primary-400 shadow-sm' 
              : 'text-gray-400 hover:text-white hover:bg-gray-800/60'
          ]"
        >
          <span class="text-xl">{{ r.meta.icon }}</span>
          <transition name="fade">
            <span v-if="!isSidebarCollapsed" class="text-sm">{{ r.meta.title }}</span>
          </transition>
          <!-- Indicador activo -->
          <div
            v-if="route.name === r.name && !isSidebarCollapsed"
            class="ml-auto w-1.5 h-1.5 rounded-full bg-primary-400 shadow-lg shadow-primary-400/50"
          />
        </router-link>
      </nav>

      <!-- Toggle sidebar -->
      <button
        @click="toggleSidebar"
        class="flex items-center justify-center p-4 border-t border-gray-800/40 text-gray-500 hover:text-white transition-colors"
      >
        <svg
          :class="['w-5 h-5 transition-transform duration-300', isSidebarCollapsed ? 'rotate-180' : '']"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
        </svg>
      </button>
    </aside>

    <!-- ===== Contenido Principal ===== -->
    <main class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="flex items-center justify-between px-8 py-5 border-b border-gray-800/40 bg-gray-950/50 backdrop-blur-sm">
        <div>
          <h2 class="text-2xl font-bold text-white">{{ currentTitle }}</h2>
          <p class="text-sm text-gray-500 mt-0.5">Sistema de Reconocimiento Facial con Análisis de Emociones</p>
        </div>
        <!-- Indicador de conexión -->
        <div class="status-badge bg-accent-500/20 text-accent-400">
          <span class="w-2 h-2 rounded-full bg-accent-400 animate-pulse"></span>
          Sistema Activo
        </div>
      </header>

      <!-- Área de contenido con scroll -->
      <div class="flex-1 overflow-y-auto p-8">
        <router-view v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Transición de páginas */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

/* Transición de fade para sidebar */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
