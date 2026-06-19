# Progress — taplink.my

## Current Status: Active Development — Pages 1-7 Done, Feature-Complete for MVP

## Pages ✅

- [x] Page 1: Landing page (scroll reveal, float animation, hero stagger)
- [x] Page 2: Login (Google OAuth via allauth)
- [x] Page 3: Onboarding modal
- [x] Page 4: Dashboard — Links, Appearance, Settings tabs + Analytics link
- [x] Page 5: Upgrade page (`/upgrade/`) — gift code + PromptPay placeholder
- [x] Page 6: Public Profile (`/@username/` dev, `username.taplink.my` prod)
- [x] Page 7: QR Code (`/dashboard/qr/`) — Free B&W + Standard full editor (qr-code-styling.js)
- [x] Page 8-alt: Analytics (`/dashboard/analytics/`) — views, clicks, chart, device breakdown
- [ ] Page 8: Admin Panel (`/admin-panel/`) — deferred

## Models ✅ (all migrated)
- UserProfile, Link, Appearance, GiftCode (accounts app — migrations 0001→0006)
- ProfileView, LinkClick (analytics_app — migration 0001)

## Key Features Status

### Done ✅
- Google OAuth + onboarding
- Dashboard 4-tab SPA (Alpine.js) — Links, Appearance, Settings
- Analytics tab → redirects to dedicated `/dashboard/analytics/` page
- Per-link color/text_color/icon_color/font_family
- 16 fonts (6 Free + 10 Standard), font picker dropdown grid
- Button styles: filled/outline/soft/shadow/glass/gradient/plain
- Avatar upload (center-crop 400×400 JPEG, 2MB limit) — POST `/dashboard/avatar/upload/`
- Background image upload (thumbnail 1920×1080 JPEG, 8MB limit) — POST `/dashboard/background/upload/`
- Drag & drop link reorder (SortableJS v1.15.2) — syncs Alpine array + POST reorder API
- Analytics: ProfileView + LinkClick models, tracking in profiles/views.py (IP hashed SHA256)
- Analytics dashboard: period filter (7d/30d/all), Chart.js line chart, per-link breakdown, device breakdown
- Rate limiting: gift code 5/h per user, uploads 20/h per user, login 20/min per IP (middleware)
- Free plan link limit: 2 (was 9999 dev) — "Upgrade" CTA replaces Add button at limit
- SubdomainMiddleware (prod routing username.taplink.my)
- Gift code system (model + admin generator + redemption endpoint)
- QR: Free (B&W PNG) + Standard (qr-code-styling.js client-side, full custom, PNG+SVG download)
- Public profile: full appearance, splash screen, watermark, SEO meta + JSON-LD
- Django admin: all models + gift code generator action
- UI: page-in animation, scroll reveal, float, spring modals, toast notifications
- requirements.txt added (pinned deps)

### Pending ❌
- `taplink-logo.png` in `static/img/` — QR editor "taplink.my logo" option (graceful fallback if missing)
- Admin Panel (Page 8) — deferred by user
- Production environment setup (SECRET_KEY, DEBUG=False, HTTPS settings)

## Known Issues / Dev Notes
- `qrcode` import: use `colormasks` (plural), not `colormask`
- testuser: Standard plan until 2027-06-16
- Dev login: `/dev-login/` (DEBUG only)
- Dev profile: `http://127.0.0.1:8000/@testuser/`
- QR page: `http://127.0.0.1:8000/dashboard/qr/`
- Analytics page: `http://127.0.0.1:8000/dashboard/analytics/`
- Deploy warnings (6): all standard prod security settings — not bugs

## Session History
- 2026-06-16 Session 1: Project init, Pages 1-4
- 2026-06-16 Session 2: Per-link fonts/colors, username change, plain button style
- 2026-06-17 Session 3: Pages 5-7, gift codes, public profile, QR editor, UX fixes
- 2026-06-17 Session 4: qr-code-styling.js, global UI (animations/transitions), drag&drop, avatar upload
- 2026-06-18 Session 5: Analytics (models+tracking+dashboard), rate limiting, free plan limit
- 2026-06-19 Session 6: Avatar crop modal (custom), YouTube bg, bg image position editor, GIF avatar
- 2026-06-19 Session 7: Dashboard UX overhaul — Links+Appearance merged, Add link modal (50+ types), compact link cards (accordion)
- 2026-06-19 Session 8: Link cards → Linktree-style (always expanded, inline inputs, bottom toolbar); Profile section → flat (avatar + inline name/bio/location + quick social icons + big Add pill); Design tab ayrıldı (Background); Avatar style + Buttons accordion kaldırıldı (Buttons ileride per-link template olarak gelecek); Nav sırası: Links → Design → Analytics → Settings
- 2026-06-20 Session 9: Iconify icon system (simple-icons + mdi), ICON_CATEGORIES (~155 icons), icon picker modal (search + category tabs + auto-fill grid), Link.icon max_length→80 (migration 0008), .claudeignore (dashboard focused)
- 2026-06-20 Session 10: Add Link modal Social category (31 platforms, Iconify icons, list layout instead of grid), Header Text + Divider link types (migration 0009: link_type field), Media embed system (Spotify/YouTube/SoundCloud/Apple Music/Deezer/Tidal/Bandcamp/Podcast/TikTok Video/Vimeo/Audiomack/PDF/My Video/My Music/Music Pre-save) — iframe embeds + HTML5 video/audio players on public profile
