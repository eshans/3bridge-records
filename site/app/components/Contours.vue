<script setup lang="ts">
/**
 * Deterministic "sonic landscape": stacked waveform contour lines.
 * Rendered as static SVG (same on server and client), gently drifted with CSS.
 */
const props = withDefaults(defineProps<{ lines?: number; seed?: number }>(), { lines: 28, seed: 3 })

const W = 1200
const H = 700

function rand(seed: number) {
  let s = seed
  return () => {
    s = (s * 16807) % 2147483647
    return (s - 1) / 2147483646
  }
}

const paths = computed(() => {
  const r = rand(props.seed * 7919)
  // a few shared "ridges" so lines feel like one landscape
  const ridges = Array.from({ length: 4 }, () => ({ x: r() * W, w: 120 + r() * 260, h: 40 + r() * 120 }))
  const out: { d: string; accent: boolean }[] = []
  for (let i = 0; i < props.lines; i++) {
    const base = 120 + (i * (H - 160)) / props.lines
    const phase = r() * Math.PI * 2
    const freq = 0.008 + r() * 0.006
    const amp = 4 + (i / props.lines) * 14
    let d = ''
    for (let x = 0; x <= W; x += 10) {
      let y = base + Math.sin(x * freq + phase) * amp
      for (const rd of ridges) {
        const k = (x - rd.x) / rd.w
        y -= rd.h * Math.exp(-k * k) * (1 - i / (props.lines * 1.4))
      }
      d += `${x === 0 ? 'M' : 'L'}${x},${y.toFixed(1)}`
    }
    out.push({ d, accent: i === Math.floor(props.lines * 0.62) })
  }
  return out
})
</script>

<template>
  <svg :viewBox="`0 0 ${W} ${H}`" preserveAspectRatio="xMidYMid slice" aria-hidden="true" class="contours">
    <g class="drift">
      <path
        v-for="(p, i) in paths"
        :key="i"
        :d="p.d"
        fill="none"
        :stroke="p.accent ? 'var(--red)' : 'currentColor'"
        :stroke-width="p.accent ? 2 : 1"
        vector-effect="non-scaling-stroke"
        :style="{ animationDelay: `${i * -0.35}s` }"
      />
    </g>
  </svg>
</template>

<style scoped>
.contours {
  width: 100%;
  height: 100%;
  color: var(--fg-faint);
}
path {
  opacity: 0.55;
  animation: breathe 9s ease-in-out infinite alternate;
}
@keyframes breathe {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-10px);
  }
}
</style>
