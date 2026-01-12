<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy'
  version: string
}

const health = ref<HealthStatus | null>(null)

async function fetchHealth() {
  try {
    const response = await fetch('/api/health')
    health.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch health:', error)
  }
}

onMounted(() => {
  fetchHealth()
  // Refresh every 30 seconds
  setInterval(fetchHealth, 30000)
})

const statusColors = {
  healthy: 'text-unraid-green',
  degraded: 'text-unraid-yellow',
  unhealthy: 'text-unraid-red'
}

const statusIcons = {
  healthy: '🟢',
  degraded: '🟡',
  unhealthy: '🔴'
}
</script>

<template>
  <header class="bg-unraid-bg-light border-b border-unraid-bg-lighter px-6 py-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <h1 class="text-xl font-bold text-unraid-orange">
          Array Balancer
        </h1>
        <span v-if="health" class="text-sm text-unraid-text-muted">
          v{{ health.version }}
        </span>
      </div>
      
      <div class="flex items-center space-x-4">
        <!-- Health Status -->
        <div v-if="health" class="flex items-center space-x-2">
          <span>{{ statusIcons[health.status] }}</span>
          <span :class="statusColors[health.status]" class="text-sm font-medium capitalize">
            {{ health.status }}
          </span>
        </div>
        
        <!-- User Menu -->
        <button class="flex items-center space-x-2 text-unraid-text-muted hover:text-unraid-text">
          <span>👤</span>
          <span>admin</span>
        </button>
      </div>
    </div>
  </header>
</template>
