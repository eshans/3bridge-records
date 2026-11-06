<script setup lang="ts">
import { byDate, fmtDate, getArtist, getRelease, releases, releasesFor, storeName } from '~/composables/catalog'

const route = useRoute()
const release = getRelease(route.params.slug as string)
if (!release) throw createError({ statusCode: 404, statusMessage: 'Release not found', fatal: true })

const credited = release.artists.map((s) => getArtist(s)!).filter(Boolean)

// chronological neighbours
const idx = releases.findIndex((r) => r.slug === release.slug)
const newer = releases[idx - 1]
const older = releases[idx + 1]

const more = [
  ...new Map(credited.flatMap((a) => releasesFor(a)).map((r) => [r.slug, r])).values(),
]
  .filter((r) => r.slug !== release.slug)
  .sort(byDate)
  .slice(0, 4)

// other titles issued on the same record (same catalog number)
const sameRecord = release.catalog
  ? releases.filter((r) => r.catalog === release.catalog && r.slug !== release.slug)
  : []

useSeoMeta({
  title: `${release.title} — ${release.artistLine}`,
  description: release.review[0]?.slice(0, 160) || `${release.title} by ${release.artistLine} on 3Bridge Records.`,
  ogImage: release.cover,
  ogType: 'music.album',
})

useHead({
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'MusicAlbum',
        name: release.title,
        byArtist: credited.map((a) => ({ '@type': 'MusicGroup', name: a.name })),
        datePublished: release.date ?? undefined,
        recordLabel: '3Bridge Records',
        catalogNumber: release.catalog ?? undefined,
        numTracks: release.tracks.length || undefined,
        track: release.tracks.map((t, i) => ({ '@type': 'MusicRecording', name: t.title, position: i + 1 })),
      }),
    },
  ],
})
</script>

<template>
  <article v-if="release" class="wrap pt-10">
    <nav class="meta mb-8 flex items-center gap-2" aria-label="Breadcrumb">
      <NuxtLink to="/releases" class="hover:text-red">Releases</NuxtLink>
      <span>/</span>
      <span class="truncate text-fg">{{ release.title }}</span>
    </nav>

    <div class="grid gap-10 md:grid-cols-12">
      <div class="md:col-span-6 lg:col-span-5">
        <div class="md:sticky md:top-24">
          <img
            :src="release.cover ?? ''"
            :alt="`${release.title} cover art`"
            width="1000"
            height="1000"
            class="aspect-square w-full object-cover"
            fetchpriority="high"
          />
        </div>
      </div>

      <div class="md:col-span-6 lg:col-span-7">
        <p class="meta">
          <template v-if="release.catalog"><span class="text-fg">{{ release.catalog }}</span> · </template>
          <span class="text-red-ink">{{ release.date ? fmtDate(release.date, 'long') : 'Release date unknown' }}</span><template v-if="release.tracks.length"> · {{ release.tracks.length }} {{ release.tracks.length === 1 ? 'track' : 'tracks' }}</template>
        </p>
        <h1 class="display mt-4 text-[clamp(3.5rem,9vw,8rem)]">{{ release.title }}</h1>
        <p class="mt-4 text-2xl">
          <template v-for="(a, i) in credited" :key="a.slug">
            <NuxtLink :to="`/artist/${a.slug}`" class="underline decoration-rule decoration-2 underline-offset-4 hover:text-red hover:decoration-red">{{ a.name }}</NuxtLink><span v-if="i < credited.length - 1">, </span>
          </template>
          <span v-if="!credited.length">{{ release.artistLine }}</span>
        </p>
        <p v-if="sameRecord.length" class="meta mt-4">
          Also on {{ release.catalog }}:
          <template v-for="(r, i) in sameRecord" :key="r.slug">
            <NuxtLink :to="`/release/${r.slug}`" class="text-fg underline underline-offset-4 hover:text-red">{{ r.title }}</NuxtLink><span v-if="i < sameRecord.length - 1">, </span>
          </template>
        </p>

        <div class="mt-8 flex flex-wrap gap-3">
          <a v-if="release.buyUrl" :href="release.buyUrl" target="_blank" rel="noopener" class="btn btn-red">
            Buy on {{ storeName(release.buyUrl) }} ↗
          </a>
          <a
            :href="`https://soundcloud.com/search?q=${encodeURIComponent(`${release.artistLine} ${release.title}`)}`"
            target="_blank"
            rel="noopener"
            class="btn"
          >
            Find on SoundCloud ↗
          </a>
        </div>

        <section v-if="release.tracks.length" class="mt-14">
          <h2 class="meta mb-3 border-b border-rule pb-2">Tracklist · {{ release.tracks.length }}</h2>
          <ol>
            <li
              v-for="t in release.tracks"
              :key="t.n + t.title"
              class="flex items-baseline gap-5 border-b border-rule py-3"
            >
              <span class="meta w-6 shrink-0 text-red-ink">{{ t.n.padStart(2, '0') }}</span>
              <span class="flex-1 text-lg">{{ t.title }}</span>
              <span v-if="t.duration" class="meta">{{ t.duration }}</span>
            </li>
          </ol>
        </section>

        <section v-if="release.review.length" class="mt-14">
          <h2 class="meta mb-3 border-b border-rule pb-2">Notes</h2>
          <div class="prose-3b max-w-prose text-lg leading-relaxed text-fg/85">
            <p v-for="(p, i) in release.review" :key="i">{{ p }}</p>
          </div>
        </section>
      </div>
    </div>

    <section v-if="more.length" class="mt-28">
      <h2 class="display mb-8 border-b border-rule pb-4 text-5xl md:text-7xl">
        More from {{ credited.length === 1 ? credited[0]!.name : 'these artists' }}
      </h2>
      <div class="grid grid-cols-2 gap-x-4 gap-y-10 md:grid-cols-4">
        <ReleaseCard v-for="r in more" :key="r.slug" :release="r" />
      </div>
    </section>

    <nav class="mt-24 grid grid-cols-2 border-y border-rule" aria-label="Adjacent releases">
      <NuxtLink v-if="older" :to="`/release/${older.slug}`" class="group border-r border-rule py-6 pr-4">
        <span class="meta">← Previous</span>
        <span class="mt-1 block truncate text-xl font-semibold group-hover:text-red">{{ older.title }}</span>
      </NuxtLink>
      <span v-else class="border-r border-rule" />
      <NuxtLink v-if="newer" :to="`/release/${newer.slug}`" class="group py-6 pl-4 text-right">
        <span class="meta">Next →</span>
        <span class="mt-1 block truncate text-xl font-semibold group-hover:text-red">{{ newer.title }}</span>
      </NuxtLink>
    </nav>
  </article>
</template>
