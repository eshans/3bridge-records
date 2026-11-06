import releasesData from '~~/content/releases.json'
import artistsData from '~~/content/artists.json'

export interface Track {
  n: string
  title: string
  duration: string | null
}
export interface Release {
  slug: string
  title: string
  artistLine: string
  artists: string[]
  date: string | null
  buyUrl: string | null
  cover: string | null
  thumb: string | null
  review: string[]
  tracks: Track[]
  seq: number
  catalog?: string | null
}
export interface Artist {
  slug: string
  name: string
  photo: string | null
  photoFallback?: string | null
  bio: string[]
  links: Record<string, string>
  releases: string[]
}

export const releases = releasesData as Release[]
export const artists = artistsData as Artist[]

const releaseMap = new Map(releases.map((r) => [r.slug, r]))
const artistMap = new Map(artists.map((a) => [a.slug, a]))

export const getRelease = (slug: string) => releaseMap.get(slug)
export const getArtist = (slug: string) => artistMap.get(slug)

export const releasesFor = (artist: Artist) =>
  artist.releases.map((s) => releaseMap.get(s)!).filter(Boolean).sort(byDate)

export function byDate(a: Release, b: Release) {
  return (b.date ?? '').localeCompare(a.date ?? '')
}

export const site = {
  name: '3Bridge Records',
  tagline: 'Sonic Landscapes from Brooklyn NY',
  demoEmail: 'eric@3bridgerecords.com',
  infoEmail: 'info@3bridgerecords.com',
  founded: 2013,
  sister: { name: '3Bridge Elements', url: 'https://www.3bridgelements.com' },
  social: [
    { name: 'Beatport', url: 'https://www.beatport.com/label/3bridge-records/32415' },
    { name: 'SoundCloud', url: 'https://soundcloud.com/3bridge-records' },
    { name: 'Instagram', url: 'https://www.instagram.com/3bridge_records/' },
    { name: 'Facebook', url: 'https://www.facebook.com/3BridgeRecords' },
  ],
}

export const seq = (n: number) => String(n).padStart(3, '0')

export function fmtDate(iso: string | null, style: 'short' | 'long' = 'short') {
  if (!iso) return '—'
  const [y, m, d] = iso.split('-')
  if (style === 'short') return `${d}.${m}.${y}`
  return new Date(`${iso}T12:00:00Z`).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC',
  })
}

export function storeName(url: string | null) {
  if (!url) return null
  if (url.includes('beatport')) return 'Beatport'
  if (url.includes('traxsource')) return 'Traxsource'
  return 'Store'
}

export const year =(iso: string | null) => (iso ? iso.slice(0, 4) : null)

export const linkLabel: Record<string, string> = {
  website: 'Website',
  soundcloud: 'SoundCloud',
  facebook: 'Facebook',
  twitter: 'Twitter',
  myspace: 'MySpace',
  youtube: 'YouTube',
  beatport: 'Beatport',
  instagram: 'Instagram',
}
