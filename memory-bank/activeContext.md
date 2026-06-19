# Active Context — taplink.my

## Current Status
**Phase: Active Development — Pages 1-7 complete + full link system, Page 8 (Admin Panel) deferred**

## What Was Built (2026-06-20, Session 10)

### Iconify Icon System (Session 9)
- Replaced Material Symbols icon picker with Iconify v3 CDN runtime
- `Link.icon` format: `prefix:name` (e.g. `simple-icons:instagram`, `mdi:link`)
- ICON_CATEGORIES: ~155 icons across social/commerce/media/contact/general
- Icon picker modal: search bar + category pill tabs + auto-fill grid (72px cells)
- Backward compat: old Material icons (`link.icon.includes(':')` check) still render
- Migration 0008: `Link.icon` max_length 40→80, default 'mdi:link'
- `profiles/views.py`: `is_iconify = ':' in link.icon`, `is_material = ':' not in link.icon and icon_type == 'material'`

### Add Link Modal — Social Category (Session 10)
- 31 social platforms with Iconify icons and brand colors
- List layout (not grid): `[icon badge] Platform name [›]`
- Platforms: Instagram, TikTok, TikTok Shop, X, Threads, Facebook, YouTube, LinkedIn, Snapchat, Pinterest, Twitch, Reddit, Discord, Telegram, WhatsApp, Line, WeChat, Bluesky, Mastodon, BeReal, Kick, Clubhouse, Cameo, Substack, Medium, Patreon, GitHub, Behance, Dribbble, Google Reviews, RSS Feed

### Header Text + Divider Link Types (Session 10)
- `Link.link_type` field added (migration 0009): `'link'`, `'header'`, `'divider'`
- Header card: drag handle + title input (no URL, no icon) — renders as uppercase section label on profile
- Divider card: drag handle + two lines flanking optional label — renders as hr on profile
- Dashboard card condition: `link_type !== 'header' && link_type !== 'divider'` → normal card

### Media Embed System (Session 10)
- `EMBED_LINK_TYPES` JS Set + `_get_embed(link)` Python function in `profiles/views.py`
- **iframe embeds**: Spotify (152px track / 352px album), YouTube video+playlist (315px), SoundCloud visual (300px), Apple Music (450px), Deezer (300px), Tidal (300px), Bandcamp (120px), Podcast/Spotify episode (232px), TikTok Video (700px), Vimeo (315px), Audiomack (252px), PDF via Google Docs viewer (600px)
- **HTML5 players**: My Video → `<video>` tag, My Music → `<audio>` tag with card UI
- **Styled links**: Music Pre-save → green gradient button + PRE-SAVE badge, Netflix/Disney+/Prime Video/Apple TV+/Crunchyroll/Mubi/Plex → regular links
- Fallback: if URL can't be parsed → normal link button
- Dashboard: EMBED green badge in toolbar for all embed link types

## Key File Locations
- `templates/dashboard/home.html` — entire dashboard SPA (~1800+ lines)
- `profiles/views.py` — `_get_embed()`, `public_profile()`, `_parse_youtube_id()`
- `accounts/models.py` — Link model with `link_type` field
- `accounts/migrations/` — 0001→0009 (latest: link_type field)
- `templates/profiles/public_profile.html` — public profile with embed rendering
- `.claudeignore` — dashboard-focused (profiles/, core/, analytics_app/ excluded)

## ADD_LINK_TYPES Structure
Each entry: `{ id, label, icon (Iconify ID), icon_type, color, category, link_type? }`
- category: 'social' | 'media' | 'text' | 'commerce' | 'contact' | 'events'
- link_type (optional): 'header' | 'divider' | 'spotify' | 'youtube' | 'soundcloud' | 'apple_music' | 'deezer' | 'tidal' | 'bandcamp' | 'podcast' | 'tiktok_video' | 'vimeo' | 'audiomack' | 'pdf' | 'video' | 'audio' | 'presave'

## Next Up
- Commerce category links (Shopify, Etsy, Amazon, Ko-fi, Buy Me a Coffee, Gumroad, etc.)
- Contact category (email, phone, WhatsApp Business, Calendly booking, Zoom, etc.)
- Booking system (Cal.com embed modal)
- Design tab — Text + Colors sections (currently "coming soon")
- Theme cards (8 premium placeholders need real data)

## Active Decisions / Known Quirks
- TikTok embed uses `tiktok.com/embed/v2/ID` — may not work in all browsers (CSP)
- Bandcamp embed URL construction is approximate — complex album_id requirement bypassed
- `video:` and `audio:` sentinels in embed_url field for template branching (not stored in DB)
- `colormasks` import (plural) — qrcode library quirk
- testuser: Standard plan until 2027-06-16
- Dev URLs: `http://127.0.0.1:8000/@testuser/`, `/dashboard/`, `/dashboard/analytics/`, `/dashboard/qr/`
