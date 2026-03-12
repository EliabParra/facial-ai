/**
 * Definición de rutas de la aplicación.
 *
 * Usa lazy-loading para las vistas pesadas (Reconocimiento y Reportes)
 * con el fin de reducir el bundle inicial.
 */

import RegistroView from '../views/RegistroView.vue'

export const routes = [
  {
    path: '/',
    name: 'registro',
    component: RegistroView,
    meta: { title: 'Registro', icon: '👤' },
  },
  {
    path: '/reconocimiento',
    name: 'reconocimiento',
    component: () => import('../views/ReconocimientoView.vue'),
    meta: { title: 'Reconocimiento', icon: '🎯' },
  },
  {
    path: '/reportes',
    name: 'reportes',
    component: () => import('../views/ReportesView.vue'),
    meta: { title: 'Reportes', icon: '📊' },
  },
]
