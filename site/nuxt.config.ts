import tailwindcss from '@tailwindcss/vite'
import releases from './content/releases.json'
import artists from './content/artists.json'

const SITE_URL = 'https://www.3bridgerecords.com'

export default defineNuxtConfig({
  compatibilityDate: '2026-11-01',
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  vite: { plugins: [tailwindcss()] },

  runtimeConfig: { public: { siteUrl: SITE_URL } },

  app: {
    head: {
      htmlAttrs: { lang: 'en' },
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'theme-color', content: '#0a0a0a' },
      ],
      link: [{ rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
      // set theme before paint to avoid a flash
      script: [
        {
          innerHTML:
            "try{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}catch(e){}",
          tagPosition: 'head',
        },
      ],
    },
  },

  // Keep the old WordPress URLs working
  routeRules: {
    '/about-2': { redirect: '/about' },
    '/about-2/': { redirect: '/about' },
    '/video': { redirect: '/' },
    '/events': { redirect: '/' },
    '/gallery': { redirect: '/' },
    '/gallery/**': { redirect: '/' },
    '/feed': { redirect: '/' },
  },

  nitro: {
    prerender: {
      crawlLinks: true,
      routes: [
        '/',
        '/releases',
        '/artists',
        '/about',
        '/contact',
        ...releases.map((r) => `/release/${r.slug}`),
        ...artists.map((a) => `/artist/${a.slug}`),
      ],
    },
  },
})
