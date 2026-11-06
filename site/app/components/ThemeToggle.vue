<script setup lang="ts">
const theme = ref<'dark' | 'light'>('dark')

onMounted(() => {
  theme.value = document.documentElement.dataset.theme === 'light' ? 'light' : 'dark'
})

function toggle() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  document.documentElement.dataset.theme = theme.value
  try {
    localStorage.setItem('theme', theme.value)
  } catch {}
}
</script>

<template>
  <button
    type="button"
    class="meta flex items-center gap-2 hover:text-fg"
    :aria-label="`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`"
    @click="toggle"
  >
    <span class="relative block h-3 w-3 rounded-full border border-current overflow-hidden">
      <span class="absolute inset-y-0 left-0 w-1/2 bg-current" />
    </span>
    <span class="hidden sm:inline">{{ theme === 'dark' ? 'Light' : 'Dark' }}</span>
  </button>
</template>
