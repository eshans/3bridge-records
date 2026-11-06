<script setup lang="ts">
const nav = [
  { to: '/releases', label: 'Releases' },
  { to: '/artists', label: 'Artists' },
  { to: '/about', label: 'About' },
  { to: '/contact', label: 'Contact' },
]
const open = ref(false)
const route = useRoute()
watch(() => route.fullPath, () => (open.value = false))
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-rule bg-bg/90 backdrop-blur-md">
    <div class="wrap flex h-16 items-center justify-between gap-6">
      <NuxtLink to="/" class="text-[1.9rem]" aria-label="3Bridge Records — home">
        <Logo :records="false" />
      </NuxtLink>

      <nav class="hidden md:block" aria-label="Main">
        <ul class="flex items-center gap-8">
          <li v-for="item in nav" :key="item.to">
            <NuxtLink :to="item.to" class="navlink meta text-[0.78rem] text-fg">
              <span class="bracket">3</span>{{ item.label }}<span class="bracket e3">3</span>
            </NuxtLink>
          </li>
        </ul>
      </nav>

      <div class="flex items-center gap-5">
        <ThemeToggle />
        <button
          type="button"
          class="meta text-fg md:hidden"
          :aria-expanded="open"
          aria-controls="mobile-nav"
          @click="open = !open"
        >
          {{ open ? 'Close' : 'Menu' }}
        </button>
      </div>
    </div>

    <Transition name="drop">
      <nav v-if="open" id="mobile-nav" class="border-t border-rule bg-bg md:hidden" aria-label="Main">
        <ul class="wrap py-4">
          <li v-for="(item, i) in nav" :key="item.to" class="border-b border-rule last:border-0">
            <NuxtLink :to="item.to" class="flex items-baseline justify-between py-3">
              <span class="display text-5xl">{{ item.label }}</span>
              <span class="meta">0{{ i + 1 }}</span>
            </NuxtLink>
          </li>
        </ul>
      </nav>
    </Transition>
  </header>
</template>

<style scoped>
.navlink {
  display: inline-flex;
  align-items: center;
  gap: 0.35em;
  transition: color 0.2s;
}
.bracket {
  color: var(--red);
  font-family: var(--font-sans);
  font-weight: 800;
  font-variation-settings: 'wdth' 62;
  font-size: 1.15em;
  opacity: 0;
  transition: opacity 0.2s, transform 0.25s var(--ease-snap);
}
.bracket:not(.e3) {
  transform: translateX(4px);
}
.bracket.e3 {
  transform: scaleX(-1) translateX(4px);
}
.navlink:hover .bracket,
.navlink.router-link-active .bracket {
  opacity: 1;
  transform: none;
}
.navlink:hover .bracket.e3,
.navlink.router-link-active .bracket.e3 {
  transform: scaleX(-1);
}
.drop-enter-active,
.drop-leave-active {
  transition: opacity 0.2s, transform 0.25s var(--ease-snap);
}
.drop-enter-from,
.drop-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
