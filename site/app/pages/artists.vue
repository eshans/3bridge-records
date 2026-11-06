<script setup lang="ts">
import { type Artist, artists, releasesFor, year } from '~/composables/catalog'

useSeoMeta({
  title: 'Artists',
  description: `The ${artists.length} artists who have released on 3Bridge Records.`,
})

const span = (a: Artist) => {
  const ys = releasesFor(a).map((r) => year(r.date)).filter(Boolean) as string[]
  if (!ys.length) return ''
  const lo = ys.at(-1)
  const hi = ys[0]
  return lo === hi ? lo : `${lo}–${hi}`
}

const groups = computed(() => {
  const m = new Map<string, Artist[]>()
  for (const a of artists) {
    const ch = /[a-z]/i.test(a.name[0]!) ? a.name[0]!.toUpperCase() : '#'
    if (!m.has(ch)) m.set(ch, [])
    m.get(ch)!.push(a)
  }
  return [...m.entries()]
})

const hover = ref<Artist | null>(null)
const pos = reactive({ x: 0, y: 0 })
function onMove(e: MouseEvent) {
  pos.x = e.clientX
  pos.y = e.clientY
}
</script>

<template>
  <div class="wrap pt-14">
    <header class="grid gap-6 border-b border-rule pb-8 md:grid-cols-12 md:items-end">
      <h1 class="display text-[clamp(4.5rem,15vw,12rem)] md:col-span-8">Artists</h1>
      <p class="meta md:col-span-4 md:text-right">{{ artists.length }} artists · A–Z</p>
    </header>

    <nav class="meta sticky top-16 z-30 -mx-4 flex gap-3 overflow-x-auto border-b border-rule bg-bg/95 px-4 py-3 backdrop-blur md:-mx-8 md:px-8" aria-label="Jump to letter">
      <a v-for="[ch] in groups" :key="ch" :href="`#l-${ch}`" class="hover:text-red">{{ ch }}</a>
    </nav>

    <div @mousemove="onMove" @mouseleave="hover = null">
      <section v-for="[ch, list] in groups" :id="`l-${ch}`" :key="ch" class="grid scroll-mt-32 grid-cols-[3rem_1fr] border-b border-rule md:grid-cols-12">
        <h2 class="display pt-4 text-4xl text-red md:col-span-1">{{ ch }}</h2>
        <ul class="md:col-span-11">
          <li v-for="a in list" :key="a.slug" class="border-b border-rule last:border-0">
            <NuxtLink
              :to="`/artist/${a.slug}`"
              class="group flex items-center gap-4 py-3"
              @mouseenter="hover = a"
            >
              <img
                :src="a.photo ?? a.photoFallback ?? ''"
                alt=""
                width="48"
                height="48"
                loading="lazy"
                class="aspect-square w-12 object-cover grayscale md:hidden"
              />
              <span class="display min-w-0 flex-1 pt-[0.12em] text-[clamp(1.7rem,5vw,3.6rem)] !leading-[0.95] transition-colors group-hover:text-red">
                {{ a.name }}
              </span>
              <span class="meta hidden w-28 shrink-0 text-right sm:block">{{ span(a) }}</span>
              <span class="meta w-14 shrink-0 text-right">{{ a.releases.length }} rel.</span>
            </NuxtLink>
          </li>
        </ul>
      </section>
    </div>

    <ClientOnly>
      <img
        v-if="hover && (hover.photo || hover.photoFallback)"
        :src="(hover.photo || hover.photoFallback)!"
        alt=""
        class="pointer-events-none fixed z-50 hidden aspect-[4/5] w-64 object-cover shadow-2xl md:block"
        :style="{ left: `${pos.x + 28}px`, top: `${pos.y - 160}px` }"
      />
    </ClientOnly>
  </div>
</template>
