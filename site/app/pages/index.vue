<script setup lang="ts">
import { artists, fmtDate, releases, site, storeName } from '~/composables/catalog'

const latest = releases[0]!
const recent = releases.slice(1, 9)
const roster = [...artists].sort((a, b) => b.releases.length - a.releases.length).slice(0, 12)
const years = new Set(releases.map((r) => r.date?.slice(0, 4)).filter(Boolean))

useSeoMeta({
  title: undefined,
  description:
    'Brooklyn-based electronic, house and techno label releasing underground music from international artists since 2013.',
  ogImage: latest.cover,
})
</script>

<template>
  <div>
    <!-- HERO -->
    <section class="relative overflow-hidden border-b border-rule">
      <div class="pointer-events-none absolute inset-0">
        <Contours :lines="30" />
      </div>
      <div class="wrap relative grid gap-10 pb-12 pt-14 md:grid-cols-12 md:pb-20 md:pt-24">
        <div class="md:col-span-7">
          <p class="meta mb-6"><span class="text-red">●</span> Brooklyn, NY — Est. {{ site.founded }}</p>
          <h1 class="display text-[clamp(3.6rem,12vw,10.5rem)]">
            Sonic<br />Landscapes<br /><span class="text-red">from</span> Brooklyn
          </h1>
          <p class="mt-8 max-w-md text-lg text-muted">
            An underground house &amp; techno label releasing music from international artists, and
            producing events in NYC.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <NuxtLink to="/releases" class="btn btn-red">Browse releases →</NuxtLink>
            <a :href="site.social[1]!.url" target="_blank" rel="noopener" class="btn">Listen on SoundCloud ↗</a>
          </div>
        </div>

        <!-- latest release -->
        <NuxtLink :to="`/release/${latest.slug}`" class="group self-end md:col-span-5">
          <div class="flex items-center justify-between border-b border-rule pb-2">
            <span class="meta text-red-ink">Latest release</span>
            <span class="meta">{{ latest.catalog ?? latest.date?.slice(0, 4) }}</span>
          </div>
          <div class="relative mt-4 overflow-hidden">
            <img
              :src="latest.cover ?? ''"
              :alt="`${latest.title} cover art`"
              width="1000"
              height="1000"
              class="aspect-square w-full object-cover transition-transform duration-700 ease-snap group-hover:scale-[1.03]"
              fetchpriority="high"
            />
          </div>
          <div class="mt-4 flex items-end justify-between gap-4">
            <div>
              <p class="display text-5xl group-hover:text-red">{{ latest.title }}</p>
              <p class="mt-1 text-muted">{{ latest.artistLine }}</p>
            </div>
            <p class="meta text-right">{{ fmtDate(latest.date) }}<br />{{ storeName(latest.buyUrl) ?? '' }}</p>
          </div>
        </NuxtLink>
      </div>
    </section>

    <Marquee :items="['House', 'Techno', 'Melodic', 'Deep-tech', 'Minimal', 'Brooklyn NY']" />

    <!-- RECENT -->
    <section class="wrap mt-24">
      <div class="mb-8 flex items-end justify-between gap-4 border-b border-rule pb-4">
        <h2 class="display text-6xl md:text-8xl">Recent</h2>
        <NuxtLink to="/releases" class="meta hover:text-red">All {{ releases.length }} releases →</NuxtLink>
      </div>
      <div class="grid grid-cols-2 gap-x-4 gap-y-10 md:grid-cols-4">
        <ReleaseCard v-for="r in recent" :key="r.slug" :release="r" />
      </div>
    </section>

    <!-- NUMBERS -->
    <section class="wrap mt-28">
      <dl class="grid grid-cols-2 border-t border-rule md:grid-cols-4">
        <div v-for="stat in [
          { k: 'Releases', v: releases.length },
          { k: 'Artists', v: artists.length },
          { k: 'Years active', v: years.size },
          { k: 'Boroughs', v: 3 },
        ]" :key="stat.k" class="border-b border-rule py-6 pr-4 md:border-b-0 md:border-r md:px-6 md:first:pl-0 md:last:border-r-0">
          <dt class="meta">{{ stat.k }}</dt>
          <dd class="display mt-2 text-7xl md:text-8xl">{{ stat.v }}</dd>
        </div>
      </dl>
    </section>

    <!-- ROSTER -->
    <section class="wrap mt-28">
      <div class="mb-8 flex items-end justify-between gap-4 border-b border-rule pb-4">
        <h2 class="display text-6xl md:text-8xl">Roster</h2>
        <NuxtLink to="/artists" class="meta hover:text-red">All {{ artists.length }} artists →</NuxtLink>
      </div>
      <ul class="flex flex-wrap gap-x-5 gap-y-1">
        <li v-for="a in roster" :key="a.slug">
          <NuxtLink :to="`/artist/${a.slug}`" class="display text-[clamp(2.2rem,6vw,4.75rem)] text-faint transition-colors hover:text-fg">
            {{ a.name }}<sup class="meta ml-1 align-super text-red-ink">{{ a.releases.length }}</sup>
          </NuxtLink>
        </li>
      </ul>
    </section>

    <!-- DEMOS / SISTER -->
    <section class="wrap mt-28 grid gap-4 md:grid-cols-2">
      <div class="bg-red p-8 text-on-red md:p-12">
        <p class="meta !text-on-red/80">Always listening</p>
        <h2 class="display mt-4 text-6xl md:text-7xl">Send us your demos</h2>
        <p class="mt-6 max-w-sm">
          House, techno, melodic, deep-tech, minimal: we’re interested in every style that pushes past the traditional.
        </p>
        <a :href="`mailto:${site.demoEmail}`" class="mt-8 inline-block border-b-2 border-current font-semibold">{{ site.demoEmail }}</a>
      </div>
      <a :href="site.sister.url" target="_blank" rel="noopener" class="group border border-rule p-8 transition-colors hover:border-fg md:p-12">
        <p class="meta">Sister label</p>
        <h2 class="display mt-4 text-6xl md:text-7xl">3Bridge<br />Elements ↗</h2>
        <p class="mt-6 max-w-sm text-muted">Ambient, downtempo and meditative music from the same Brooklyn crew.</p>
      </a>
    </section>
  </div>
</template>
