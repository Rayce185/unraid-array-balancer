<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Permissions {
  running_as_uid: number
  running_as_gid: number
  all_passed: boolean
  has_critical_failures: boolean
  checks: Array<{
    name: string
    description: string
    status: string
    error: string | null
  }>
}

const permissions = ref<Permissions | null>(null)

async function fetchPermissions() {
  try {
    const response = await fetch('/api/permissions')
    permissions.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch permissions:', error)
  }
}

onMounted(fetchPermissions)

const statusColors: Record<string, string> = {
  ok: 'text-unraid-green',
  warning: 'text-unraid-yellow',
  error: 'text-unraid-red'
}

const statusIcons: Record<string, string> = {
  ok: '✅',
  warning: '⚠️',
  error: '❌'
}
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Settings</h2>
    
    <!-- Permission Status -->
    <div class="card mb-6">
      <h3 class="text-lg font-semibold mb-4">Permission Status</h3>
      
      <div v-if="permissions">
        <div class="mb-4">
          <p class="text-sm text-unraid-text-muted">
            Running as UID: {{ permissions.running_as_uid }}, GID: {{ permissions.running_as_gid }}
          </p>
        </div>
        
        <div class="space-y-3">
          <div
            v-for="check in permissions.checks"
            :key="check.name"
            class="flex items-center justify-between p-3 bg-unraid-bg rounded"
          >
            <div class="flex items-center space-x-3">
              <span>{{ statusIcons[check.status] }}</span>
              <div>
                <p class="font-medium">{{ check.description }}</p>
                <p v-if="check.error" class="text-sm text-unraid-red">{{ check.error }}</p>
              </div>
            </div>
            <span :class="statusColors[check.status]" class="capitalize">
              {{ check.status }}
            </span>
          </div>
        </div>
      </div>
      
      <div v-else class="text-unraid-text-muted">
        Loading permissions...
      </div>
    </div>
    
    <!-- About -->
    <div class="card">
      <h3 class="text-lg font-semibold mb-4">About</h3>
      <p class="text-unraid-text-muted mb-2">
        unRAID Array Balancer v0.1.0-alpha
      </p>
      <p class="text-sm text-unraid-text-muted">
        A disk balancing tool for unRAID 7+ arrays.
      </p>
      <div class="mt-4 flex space-x-4">
        <a
          href="https://github.com/Rayce185/unraid-array-balancer"
          target="_blank"
          class="text-unraid-orange hover:underline"
        >
          GitHub
        </a>
        <a
          href="https://github.com/Rayce185/unraid-array-balancer/issues"
          target="_blank"
          class="text-unraid-orange hover:underline"
        >
          Report Issue
        </a>
      </div>
    </div>
  </div>
</template>
