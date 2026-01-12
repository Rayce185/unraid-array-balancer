<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

interface Disk {
  id: string
  name: string
  mount_point: string
  total_bytes: number
  used_bytes: number
  free_bytes: number
  used_percent: number
  filesystem: string | null
  is_mounted: boolean
  is_readable: boolean
  is_writable: boolean
}

interface DiskListResponse {
  disks: Disk[]
  total_count: number
  total_capacity_bytes: number
  total_used_bytes: number
  total_free_bytes: number
  average_used_percent: number
}

const diskData = ref<DiskListResponse | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

async function fetchDisks() {
  try {
    loading.value = true
    error.value = null
    const response = await fetch('/api/disks')
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    diskData.value = await response.json()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load disks'
  } finally {
    loading.value = false
  }
}

onMounted(fetchDisks)

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

function getProgressColor(percent: number): string {
  if (percent >= 95) return 'bg-unraid-red'
  if (percent >= 85) return 'bg-unraid-yellow'
  return 'bg-unraid-green'
}
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Dashboard</h2>
    
    <!-- Loading State -->
    <div v-if="loading" class="card">
      <p class="text-unraid-text-muted">Loading disk information...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="card bg-unraid-red/20 border border-unraid-red">
      <p class="text-unraid-red">{{ error }}</p>
      <button @click="fetchDisks" class="btn btn-secondary mt-4">Retry</button>
    </div>
    
    <!-- Disk Data -->
    <div v-else-if="diskData">
      <!-- Summary Cards -->
      <div class="grid grid-cols-4 gap-4 mb-6">
        <div class="card">
          <h3 class="text-sm text-unraid-text-muted mb-1">Total Disks</h3>
          <p class="text-2xl font-bold">{{ diskData.total_count }}</p>
        </div>
        <div class="card">
          <h3 class="text-sm text-unraid-text-muted mb-1">Total Capacity</h3>
          <p class="text-2xl font-bold">{{ formatBytes(diskData.total_capacity_bytes) }}</p>
        </div>
        <div class="card">
          <h3 class="text-sm text-unraid-text-muted mb-1">Used Space</h3>
          <p class="text-2xl font-bold">{{ formatBytes(diskData.total_used_bytes) }}</p>
        </div>
        <div class="card">
          <h3 class="text-sm text-unraid-text-muted mb-1">Average Usage</h3>
          <p class="text-2xl font-bold">{{ diskData.average_used_percent.toFixed(1) }}%</p>
        </div>
      </div>
      
      <!-- Disk List -->
      <div class="card">
        <h3 class="text-lg font-semibold mb-4">Array Disks</h3>
        
        <div class="space-y-4">
          <div
            v-for="disk in diskData.disks"
            :key="disk.id"
            class="p-4 bg-unraid-bg rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <span class="font-medium">{{ disk.name }}</span>
                <span class="text-sm text-unraid-text-muted">{{ disk.filesystem }}</span>
                <span v-if="!disk.is_writable" class="text-xs text-unraid-yellow">⚠️ Read-only</span>
              </div>
              <div class="text-right">
                <span class="font-medium">{{ disk.used_percent.toFixed(1) }}%</span>
                <span class="text-sm text-unraid-text-muted ml-2">
                  {{ formatBytes(disk.used_bytes) }} / {{ formatBytes(disk.total_bytes) }}
                </span>
              </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="h-4 bg-unraid-bg-lighter rounded-full overflow-hidden">
              <div
                :class="getProgressColor(disk.used_percent)"
                class="h-full transition-all duration-300"
                :style="{ width: `${disk.used_percent}%` }"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
