<script setup lang="ts">
import { fmtDate, releases, year } from '~/composables/catalog'

useSeoMeta({
  title: 'Releases',
  description: `The full 3Bridge Records discography — ${releases.length} releases of house, techno and deep electronic music.`,
})

const route = useRoute()
const router = useRouter()

// prerendered HTML has no query, so apply ?view / ?year after hydration
const view = ref<'grid' | 'index'>('grid')
const activeYear = ref<string | null>(null)
const q = ref('')
// (Nuxt hydrates with the query-less prerendered route, then swaps in the real URL)
function applyQuery() {
  view.value = route.query.view === 'index' ? 'index' : 'grid'
  activeYear.value = typeof route.query.year === 'string' ? route.query.year : null
}
onMounted(applyQuery)
watch(() => route.query, applyQuery)

const yearList = [...new Set(releases.map((r) => year(r.date)).filter(Boolean))] as string[]

const filtered = computed(() => {
  const needle = q.value.trim().toLowerCase()
  return releases.filter(
    (r) =>
      (!activeYear.value || year(r.date) === activeYear.value) &&
      (!needle || `${r.title} ${r.artistLine} ${r.tracks.map((t) => t.title).join(' ')}`.toLowerCase().includes(needle)),
  )
})

watch([view, activeYear], () => {
  router.replace({
    query: {
      ...(view.value === 'index' ? { view: 'index' } : {}),
      ...(activeYear.value ? { year: activeYear.value } : {}),
    },
  })
})

// floating cover preview for the index view
const hover = ref<string | null>(null)
const pos = reactive({ x: 0, y: 0 })
function onMove(e: MouseEvent) {
  pos.x = e.clientX
  pos.y = e.clientY
}
</script>

<template>
  <div class="wrap pt-14">
    <header class="grid gap-6 border-b border-rule pb-8 md:grid-cols-12 md:items-end">
      <h1 class="display text-[clamp(4.5rem,15vw,12rem)] md:col-span-8">Releases</h1>
      <p class="meta md:col-span-4 md:text-right">
        {{ releases.length }} records · {{ yearList.at(-1) }}–{{ yearList[0] }}
      </p>
    </header>

    <!-- controls -->
    <div class="sticky top-16 z-30 -mx-4 border-b border-rule bg-bg/95 px-4 py-3 backdrop-blur md:-mx-8 md:px-8">
      <div class="flex flex-wrap items-center gap-3">
        <label class="relative min-w-0 flex-1 md:max-w-xs">
          <span class="sr-only">Search releases</span>
          <input
            v-model="q"
            type="search"
            placeholder="Search title, artist, track…"
            class="w-full border border-rule bg-transparent px-3 py-2 font-mono text-xs placeholder:text-faint focus:border-fg focus:outline-none"
          />
        </label>
        <div class="flex border border-rule" role="group" aria-label="View">
          <button
            v-for="v in (['grid', 'index'] as const)"
            :key="v"
            type="button"
            class="meta px-3 py-2"
            :class="view === v ? 'bg-fg !text-bg' : 'hover:text-fg'"
            :aria-pressed="view === v"
            @click="view = v"
          >
            {{ v }}
          </button>
        </div>
      </div>
      <div class="mt-3 flex gap-1 overflow-x-auto pb-1" role="group" aria-label="Filter by year">
        <button
          type="button"
          class="meta shrink-0 border px-2.5 py-1"
          :class="!activeYear ? 'border-red bg-red !text-on-red' : 'border-rule hover:text-fg'"
          :aria-pressed="!activeYear"
          @click="activeYear = null"
        >
          All
        </button>
        <button
          v-for="y in yearList"
          :key="y"
          type="button"
          class="meta shrink-0 border px-2.5 py-1"
          :class="activeYear === y ? 'border-red bg-red !text-on-red' : 'border-rule hover:text-fg'"
          :aria-pressed="activeYear === y"
          @click="activeYear = activeYear === y ? null : y"
        >
          {{ y }}
        </button>
      </div>
    </div>

    <p class="meta mt-6" aria-live="polite">{{ filtered.length }} shown</p>

    <!-- GRID -->
    <div v-if="view === 'grid'" class="mt-6 grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
      <ReleaseCard v-for="(r, i) in filtered" :key="r.slug" :release="r" :eager="i < 5" />
    </div>

    <!-- INDEX -->
    <div v-else class="mt-6" @mousemove="onMove" @mouseleave="hover = null">
      <div class="meta hidden grid-cols-12 gap-4 border-b border-rule pb-2 md:grid">
        <span class="col-span-5">Title</span>
        <span class="col-span-4">Artist</span>
        <span class="col-span-2">Date</span>
        <span class="col-span-1 text-right">Tracks</span>
      </div>
      <ul>
        <li v-for="r in filtered" :key="r.slug">
          <NuxtLink
            :to="`/release/${r.slug}`"
            class="row group grid grid-cols-[3.5rem_1fr] items-center gap-x-4 gap-y-0.5 border-b border-rule py-3 md:grid-cols-12"
            @mouseenter="hover = r.thumb"
          >
            <img :src="r.thumb ?? ''" alt="" width="56" height="56" loading="lazy" class="row-span-2 aspect-square w-14 md:hidden" />
            <span class="truncate text-lg font-semibold group-hover:text-red md:col-span-5">{{ r.title }}</span>
            <span class="truncate text-muted md:col-span-4">{{ r.artistLine }}</span>
            <span class="meta hidden md:col-span-2 md:block">{{ fmtDate(r.date) }}</span>
            <span class="meta hidden text-right md:col-span-1 md:block">{{ r.tracks.length || '—' }}</span>
          </NuxtLink>
        </li>
      </ul>
      <ClientOnly>
        <img
          v-if="hover"
          :src="hover"
          alt=""
          class="pointer-events-none fixed z-50 hidden w-56 shadow-2xl md:block"
          :style="{ left: `${pos.x + 24}px`, top: `${pos.y - 112}px` }"
        />
      </ClientOnly>
    </div>

    <p v-if="!filtered.length" class="py-24 text-center text-muted">Nothing matches “{{ q }}”.</p>
  </div>
</template>
