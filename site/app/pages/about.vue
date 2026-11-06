<script setup lang="ts">
import { artists, releases, site } from '~/composables/catalog'

useSeoMeta({
  title: 'About',
  description:
    '3Bridge Records is a Brooklyn, NY label founded by Greg Cuoco and Eric Shans, releasing sounds from around the world that push the frontiers of electronic music.',
})
</script>

<template>
  <div>
    <section class="relative overflow-hidden border-b border-rule">
      <div class="pointer-events-none absolute inset-0 opacity-70">
        <Contours :lines="22" :seed="11" />
      </div>
      <div class="wrap relative pb-16 pt-14">
        <h1 class="display text-[clamp(4.5rem,15vw,12rem)]">About</h1>
        <p class="mt-10 max-w-4xl text-[clamp(1.5rem,3.2vw,2.6rem)] font-medium leading-tight">
          3Bridge is a collection of sounds from around the world that push the frontiers of electronic music,
          <span class="text-red-ink">connecting those who believe sound, visuals and the landscape around them define the creative experience.</span>
        </p>
      </div>
    </section>

    <section class="wrap mt-20 grid gap-12 md:grid-cols-12">
      <div class="md:col-span-4">
        <h2 class="meta border-b border-rule pb-2">The label</h2>
      </div>
      <div class="prose-3b max-w-prose text-lg leading-relaxed text-fg/85 md:col-span-8">
        <p>
          3Bridge Records is based in Brooklyn, NY, run by founder Greg Cuoco and Eric Shans. Since {{ site.founded }} the
          label has released {{ releases.length }} records from {{ artists.length }} artists, and produced events across
          NYC.
        </p>
        <p>
          We release music that challenges the boundaries of traditional house music. Whether it’s house, techno,
          melodic, deep-tech or minimal, we’re interested in all styles, and always looking for new, creative talent to
          build our roster.
        </p>
        <p>
          Our sister label, <a :href="site.sister.url" target="_blank" rel="noopener">3Bridge Elements</a>, focuses on
          ambient, downtempo and meditative music.
        </p>
      </div>
    </section>

    <section class="wrap mt-20 grid gap-12 md:grid-cols-12">
      <div class="md:col-span-4">
        <h2 class="meta border-b border-rule pb-2">Find us</h2>
      </div>
      <ul class="grid gap-px border border-rule bg-rule sm:grid-cols-2 md:col-span-8">
        <li v-for="s in site.social" :key="s.name" class="bg-bg">
          <a :href="s.url" target="_blank" rel="noopener" class="group flex items-center justify-between p-6">
            <span class="display text-4xl group-hover:text-red">{{ s.name }}</span>
            <span class="meta">↗</span>
          </a>
        </li>
      </ul>
    </section>
  </div>
</template>
