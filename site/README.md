# 3Bridge Records — site

Nuxt 4 static rebuild of www.3bridgerecords.com (replacing the old WordPress "Replay" theme).

```sh
npm install
npm run dev        # http://localhost:3000
npm run generate   # static site -> .output/public (deploy this folder anywhere)
```

## Content

All content is in `content/` as JSON, generated from the WordPress export:

- `content/releases.json`: 129 releases (title, artists, date, buy link, review, tracklist, cover)
- `content/artists.json`: 51 artists (bio, photo, links, release slugs)
- images: `public/media/` (resized from `../wp-export/media/`)

To regenerate the content from the saved WordPress copy:

```sh
python3 -I ../scripts/extract_content.py ../wp-export/mirror ../wp-export/media .
```

To add a release, add an entry to `content/releases.json`, put its cover in `public/media/`,
and add its slug to the artist's `releases` list in `content/artists.json`.

Label-wide copy (emails, social links, founding year) is in `app/composables/catalog.ts` (`site`).

## URLs

The old WordPress paths are kept: `/releases`, `/release/<slug>`, `/artists`, `/artist/<slug>`.
Old pages that were empty placeholders (`/video`, `/events`, `/gallery`) and `/about-2` redirect (see `routeRules` in `nuxt.config.ts`).

## Design

- Dark by default with a light theme toggle; tokens are in `app/assets/css/main.css`
- Logo colours: black, white and red (`--red`). The logo's mirrored red "3" is used as a bracket motif on nav links (`.e3`)
- Type: Archivo Variable (condensed `wdth 62` for display) + JetBrains Mono for metadata
