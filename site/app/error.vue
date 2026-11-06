<script setup lang="ts">
import type { NuxtError } from '#app'
const props = defineProps<{ error: NuxtError }>()
useSeoMeta({ title: props.error.statusCode === 404 ? 'Not found' : 'Error' })
</script>

<template>
  <div class="flex min-h-dvh flex-col">
    <SiteHeader />
    <main class="wrap flex flex-1 flex-col justify-center py-24">
      <p class="meta text-red-ink">Error {{ error.statusCode }}</p>
      <h1 class="display mt-4 text-[clamp(5rem,20vw,16rem)]">
        <span class="text-red">4</span>0<span class="text-red">4</span>
      </h1>
      <p class="mt-6 max-w-md text-lg text-muted">
        {{ error.statusCode === 404 ? 'This track isn’t on the record. It may have moved when the site was rebuilt.' : error.message }}
      </p>
      <div class="mt-8 flex gap-3">
        <button type="button" class="btn btn-red" @click="clearError({ redirect: '/' })">Home</button>
        <button type="button" class="btn" @click="clearError({ redirect: '/releases' })">Releases</button>
      </div>
    </main>
  </div>
</template>
