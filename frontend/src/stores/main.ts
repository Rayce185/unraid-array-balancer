import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMainStore = defineStore('main', () => {
  // Authentication state
  const isAuthenticated = ref(false)
  const username = ref<string | null>(null)
  
  // UI state
  const sidebarCollapsed = ref(false)
  const welcomeAccepted = ref(false)
  
  // Actions
  function setAuthenticated(value: boolean, user?: string) {
    isAuthenticated.value = value
    username.value = user ?? null
  }
  
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
  
  function acceptWelcome() {
    welcomeAccepted.value = true
    localStorage.setItem('welcomeAccepted', 'true')
  }
  
  // Initialize from localStorage
  function init() {
    welcomeAccepted.value = localStorage.getItem('welcomeAccepted') === 'true'
  }
  
  return {
    isAuthenticated,
    username,
    sidebarCollapsed,
    welcomeAccepted,
    setAuthenticated,
    toggleSidebar,
    acceptWelcome,
    init,
  }
})
