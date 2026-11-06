<script setup lang="ts">
defineProps<{ items: string[] }>()
</script>

<template>
  <div class="marquee overflow-hidden border-y border-rule bg-red text-on-red" aria-hidden="true">
    <div class="track flex w-max">
      <template v-for="n in 2" :key="n">
        <span v-for="item in items" :key="`${n}-${item}`" class="display flex items-center whitespace-nowrap px-6 py-3 text-3xl md:text-4xl">
          {{ item }}<span class="ml-12 inline-block">3</span>
        </span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.track {
  animation: scroll 38s linear infinite;
}
.marquee:hover .track {
  animation-play-state: paused;
}
@keyframes scroll {
  to {
    transform: translateX(-50%);
  }
}
</style>
