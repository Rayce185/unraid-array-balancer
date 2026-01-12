<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()

const navItems = [
  { name: 'Dashboard', path: '/', icon: '📊' },
  { name: 'File Browser', path: '/files', icon: '📁' },
  { name: 'Task Queue', path: '/tasks', icon: '📋' },
  { name: 'Settings', path: '/settings', icon: '⚙️' },
]
</script>

<template>
  <aside class="w-64 bg-unraid-bg-light border-r border-unraid-bg-lighter">
    <nav class="p-4 space-y-2">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors"
        :class="[
          route.path === item.path
            ? 'bg-unraid-orange text-white'
            : 'text-unraid-text-muted hover:bg-unraid-bg-lighter hover:text-unraid-text'
        ]"
      >
        <span class="text-lg">{{ item.icon }}</span>
        <span class="font-medium">{{ item.name }}</span>
      </RouterLink>
    </nav>
    
    <!-- Mover Status -->
    <div class="p-4 border-t border-unraid-bg-lighter">
      <div class="card">
        <h3 class="text-sm font-medium text-unraid-text-muted mb-2">Mover Status</h3>
        <div class="flex items-center space-x-2">
          <span class="text-unraid-green">●</span>
          <span class="text-sm">Idle</span>
        </div>
      </div>
    </div>
  </aside>
</template>
