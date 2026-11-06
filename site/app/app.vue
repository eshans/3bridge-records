<script setup lang="ts">
useHead({
  titleTemplate: (t?: string) => (t ? `${t} — 3Bridge Records` : '3Bridge Records — Sonic Landscapes from Brooklyn NY'),
})
useSeoMeta({ ogSiteName: '3Bridge Records', twitterCard: 'summary_large_image' })
</script>

<template>
  <div class="flex min-h-dvh flex-col">
    <a href="#main" class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:bg-red focus:px-3 focus:py-2 focus:text-on-red">
      Skip to content
    </a>
    <SiteHeader />
    <main id="main" class="flex-1">
      <NuxtPage />
    </main>
    <SiteFooter />
  </div>
</template>
