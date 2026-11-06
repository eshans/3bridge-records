<script setup lang="ts">
import { type Release, year } from '~/composables/catalog'
defineProps<{ release: Release; eager?: boolean }>()
</script>

<template>
  <NuxtLink :to="`/release/${release.slug}`" class="card group block">
    <div class="relative aspect-square overflow-hidden">
      <img
        :src="release.thumb ?? ''"
        :alt="`${release.title} cover art`"
        width="480"
        height="480"
        :loading="eager ? 'eager' : 'lazy'"
        decoding="async"
        class="h-full w-full object-cover transition-transform duration-500 ease-snap group-hover:scale-[1.04]"
      />
      <span v-if="release.catalog" class="meta absolute left-0 top-0 bg-bg px-2 py-1 !text-fg">{{ release.catalog }}</span>
      <span class="absolute inset-0 ring-1 ring-inset ring-transparent transition group-hover:ring-red" />
    </div>
    <div class="mt-3 flex items-start justify-between gap-3">
      <div class="min-w-0">
        <h3 class="truncate font-semibold leading-tight group-hover:text-red">{{ release.title }}</h3>
        <p class="truncate text-sm text-muted">{{ release.artistLine }}</p>
      </div>
      <span class="meta shrink-0 pt-0.5">{{ year(release.date) ?? '' }}</span>
    </div>
  </NuxtLink>
</template>
