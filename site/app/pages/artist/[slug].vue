<script setup lang="ts">
import { getArtist, linkLabel, releasesFor, year } from '~/composables/catalog'

const route = useRoute()
const artist = getArtist(route.params.slug as string)
if (!artist) throw createError({ statusCode: 404, statusMessage: 'Artist not found', fatal: true })

const discog = releasesFor(artist)
const photo = artist.photo ?? artist.photoFallback ?? null
const years = discog.map((r) => year(r.date)).filter(Boolean) as string[]
const first = years.at(-1)
const last = years[0]

useSeoMeta({
  title: artist.name,
  description: artist.bio[0]?.slice(0, 160) || `${artist.name} on 3Bridge Records — ${discog.length} releases.`,
  ogImage: photo,
})
</script>

<template>
  <article v-if="artist" class="pt-10">
    <div class="wrap">
      <nav class="meta mb-8 flex items-center gap-2" aria-label="Breadcrumb">
        <NuxtLink to="/artists" class="hover:text-red">Artists</NuxtLink>
        <span>/</span>
        <span class="text-fg">{{ artist.name }}</span>
      </nav>
      <h1 class="display break-words text-[clamp(4rem,14vw,13rem)]">{{ artist.name }}</h1>
    </div>

    <div class="wrap mt-10 grid gap-10 md:grid-cols-12">
      <div class="md:col-span-5">
        <img
          v-if="photo"
          :src="photo"
          :alt="artist.name"
          class="aspect-[4/5] w-full object-cover"
          fetchpriority="high"
        />
        <dl class="mt-6 grid grid-cols-2 border-t border-rule">
          <div class="border-b border-r border-rule py-4 pr-4">
            <dt class="meta">Releases</dt>
            <dd class="display mt-1 text-5xl">{{ discog.length }}</dd>
          </div>
          <div class="border-b border-rule py-4 pl-4">
            <dt class="meta">On 3Bridge</dt>
            <dd class="display mt-1 text-5xl">{{ first === last ? first : `${first}–${last?.slice(2)}` }}</dd>
          </div>
        </dl>
        <ul v-if="Object.keys(artist.links).length" class="mt-6 flex flex-wrap gap-2">
          <li v-for="(url, kind) in artist.links" :key="kind">
            <a :href="url" target="_blank" rel="noopener" class="btn !px-3 !py-2">{{ linkLabel[kind] ?? kind }} ↗</a>
          </li>
        </ul>
      </div>

      <div class="md:col-span-7">
        <h2 class="meta mb-3 border-b border-rule pb-2">Biography</h2>
        <div v-if="artist.bio.length" class="prose-3b max-w-prose text-lg leading-relaxed text-fg/85">
          <p v-for="(p, i) in artist.bio" :key="i">{{ p }}</p>
        </div>
        <p v-else class="text-muted">
          {{ artist.name }} has released {{ discog.length }} {{ discog.length === 1 ? 'record' : 'records' }} on 3Bridge Records.
        </p>
      </div>
    </div>

    <section class="wrap mt-24">
      <h2 class="display mb-8 border-b border-rule pb-4 text-5xl md:text-7xl">Discography</h2>
      <div class="grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 lg:grid-cols-4">
        <ReleaseCard v-for="r in discog" :key="r.slug" :release="r" />
      </div>
    </section>
  </article>
</template>
