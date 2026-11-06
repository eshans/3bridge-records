<script setup lang="ts">
import { site } from '~/composables/catalog'
const now = new Date().getFullYear()
</script>

<template>
  <footer class="mt-32 border-t border-rule">
    <div class="wrap grid gap-12 py-16 md:grid-cols-12">
      <div class="@container md:col-span-7">
        <p class="meta mb-4">Demos for both labels</p>
        <!-- sized to the column (cqi), so the address always fits on one line -->
        <a
          :href="`mailto:${site.demoEmail}`"
          class="display block whitespace-nowrap text-[min(8cqi,5.5rem)] hover:text-red"
        >
          {{ site.demoEmail }}
        </a>
      </div>
      <div class="grid grid-cols-2 gap-8 md:col-span-5">
        <div>
          <p class="meta mb-4">Follow</p>
          <ul class="space-y-2">
            <li v-for="s in site.social" :key="s.name">
              <a :href="s.url" target="_blank" rel="noopener" class="hover:text-red">{{ s.name }} ↗</a>
            </li>
          </ul>
        </div>
        <div>
          <p class="meta mb-4">Label</p>
          <ul class="space-y-2">
            <li><NuxtLink to="/releases" class="hover:text-red">Releases</NuxtLink></li>
            <li><NuxtLink to="/artists" class="hover:text-red">Artists</NuxtLink></li>
            <li><NuxtLink to="/about" class="hover:text-red">About</NuxtLink></li>
            <li>
              <a :href="site.sister.url" target="_blank" rel="noopener" class="hover:text-red">
                {{ site.sister.name }} ↗
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <div class="overflow-hidden border-t border-rule">
      <div class="wrap flex flex-col gap-6 py-8 md:flex-row md:items-end md:justify-between">
        <Logo class="text-[clamp(4rem,16vw,13rem)]" />
        <p class="meta">© {{ site.founded }}–{{ now }} 3Bridge Records · Brooklyn, NY</p>
      </div>
    </div>
  </footer>
</template>
