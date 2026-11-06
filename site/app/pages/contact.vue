<script setup lang="ts">
import { site } from '~/composables/catalog'

useSeoMeta({
  title: 'Contact',
  description: `Get in touch with 3Bridge Records. Send demos to ${site.demoEmail}.`,
})

const blocks = [
  { label: 'Demos', note: 'For 3Bridge Records and 3Bridge Elements', email: site.demoEmail },
  { label: 'General', note: 'Inquiries, requests and the like', email: site.infoEmail },
]
</script>

<template>
  <div class="wrap pt-14">
    <h1 class="display border-b border-rule pb-8 text-[clamp(4.5rem,15vw,12rem)]">Contact</h1>

    <div class="mt-12 grid gap-4 md:grid-cols-2">
      <a
        v-for="(b, i) in blocks"
        :key="b.label"
        :href="`mailto:${b.email}`"
        class="group flex min-h-72 flex-col justify-between p-8 transition-colors md:p-12"
        :class="i === 0 ? 'bg-red text-on-red' : 'border border-rule hover:border-fg'"
      >
        <div>
          <p class="meta" :class="i === 0 && '!text-on-red/80'">{{ b.label }}</p>
          <p class="mt-2" :class="i === 0 ? '' : 'text-muted'">{{ b.note }}</p>
        </div>
        <p class="display mt-10 text-[clamp(1.4rem,6.4vw,3.75rem)] [overflow-wrap:anywhere] lg:text-[clamp(2rem,3.4vw,3.75rem)]">{{ b.email }}</p>
      </a>
    </div>

    <p class="mt-12 max-w-xl text-muted">
      Sending a demo? A private SoundCloud or download link works best. Tell us a little about yourself and which
      label you think it fits.
    </p>
  </div>
</template>
