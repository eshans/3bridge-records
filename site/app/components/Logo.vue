<script setup lang="ts">
withDefaults(defineProps<{ records?: boolean }>(), { records: true })
</script>

<template>
  <span class="logo inline-flex flex-col leading-none" aria-label="3Bridge Records">
    <span class="display flex items-baseline" aria-hidden="true">
      <span class="text-red">3</span><span>BRIDG</span><span class="e3 text-red">3</span>
    </span>
    <span v-if="records" class="records meta" aria-hidden="true">Records</span>
  </span>
</template>

<style scoped>
.logo .display {
  font-size: 1em;
  line-height: 0.8;
}
.records {
  font-size: 0.24em;
  letter-spacing: 0.62em;
  margin-top: 0.28em;
  margin-right: -0.62em;
  color: var(--fg-muted);
  text-align: justify;
}
</style>
