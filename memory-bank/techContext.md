# Tech Context — taplink.my

## Core Technologies

### Backend
- **Django 5.x** — Main framework
- **django-allauth 65.x** — Google OAuth (`SOCIALACCOUNT_ONLY = True`, `ACCOUNT_SIGNUP_FIELDS = []`)
- **django-ratelimit 4.1.0** — Rate limiting on gift code, uploads, login
- **Pillow 12.x** — Image processing (avatar crop, background resize)
- **qrcode[pil] 8.x** — Server-side QR for Free plan download
- **PyJWT** — Required by allauth

### Frontend
- **Django Templates** — Server-side rendering
- **TailwindCSS v3 CDN** — `https://cdn.tailwindcss.com?plugins=forms,container-queries`
- **Alpine.js v3 CDN** — `https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js`
- **Alpine Collapse plugin** — loaded BEFORE Alpine
- **SortableJS v1.15.2 CDN** — drag & drop link reorder (dashboard only)
- **qr-code-styling@1.6.0-rc.1 CDN** — client-side QR for Standard plan (qr.html only)
- **Chart.js 4.4.3 CDN** — analytics charts (analytics.html only)
- **Material Symbols Outlined** — Google Fonts icon font
- **Inter** — Primary font (base.html)
- **Public profile** — Standalone HTML (no base.html), minimal JS, Tailwind NOT used (inline styles)

### Infrastructure
- **SQLite** (dev) — `db.sqlite3` in project root
- **Caddy** — Planned for prod (wildcard SSL `*.taplink.my`)
- No build pipeline — CDN only

### Authentication
- Google OAuth 2.0 only via allauth
- Adapter: `accounts.adapters.TaplinkSocialAccountAdapter`

## Project Structure (actual)
```
config/
  settings.py   — Main settings (SECRET_KEY + DEBUG from env vars)
  urls.py       — Root URL config
  wsgi.py / asgi.py
core/
  urls.py       — landing, upgrade, upgrade/redeem, privacy, terms, dev-login
  views.py      — landing, upgrade, redeem_gift_code (rate limited 5/h), privacy, terms, dev_login
accounts/
  models.py     — UserProfile, Link, Appearance, GiftCode + signals
  adapters.py   — TaplinkSocialAccountAdapter
  admin.py      — All models; GiftCodeAdmin with bulk generate action
  views.py      — onboarding, check_username
  urls.py       — onboarding/, check-username/
  migrations/   — 0001..0006
dashboard/
  views.py      — home, link CRUD, appearance_save, settings_save, username_change,
                  account_delete, link_reorder, avatar_upload (rl 20/h), background_upload (rl 20/h),
                  qr_page, qr_preview, qr_download, analytics
  urls.py       — 13 URL patterns
profiles/
  views.py      — public_profile (records ProfileView), link_redirect (records LinkClick)
  urls.py       — /@<username>/, /@<username>/r/<link_id>/
  middleware.py — SubdomainMiddleware + LoginRateLimitMiddleware (20/min per IP on login URLs)
analytics_app/
  models.py     — ProfileView (user, ip_hash, device, created_at)
                  LinkClick (user, link_id, link_title, ip_hash, device, created_at)
  migrations/   — 0001_initial
templates/
  base.html                        — Indigo Dark design system, Alpine, Tailwind config,
                                     page-in/float/modal/reveal animations, showToast()
  core/landing.html                — Scroll reveal + hero stagger animations
  core/upgrade.html                — Gift code UI + comparison table
  core/privacy.html / terms.html
  account/login.html
  accounts/onboarding.html
  dashboard/home.html              — ~1300 lines, full dashboard SPA
                                     SortableJS drag&drop, avatar/bg upload, tab transitions
  dashboard/qr.html                — Free server-side + Standard qr-code-styling.js
  dashboard/analytics.html         — Chart.js, period filter, per-link breakdown
  profiles/public_profile.html     — Standalone, inline styles, no base.html
  profiles/not_found.html / paused.html
  admin/accounts/giftcode/         — Custom generate page + changelist button
memory-bank/    — This documentation system
```

## Indigo Dark Design System (in base.html tailwind.config)
Key color tokens:
- `primary: #c0c1ff`, `on-primary: #1000a9`
- `primary-container: #8083ff`
- `background: #13131b`, `surface: #13131b`
- `surface-container: #1f1f27`, `surface-container-high: #292932`
- `surface-container-low: #1a1a22`
- `outline-variant: #464554`
- `error: #ffb4ab`, `tertiary: #ffb783`
- `secondary: #cbc2db`, `on-secondary-container: #e8def8`

Key CSS classes:
- `.brand-glow` — `box-shadow: 0 0 20px rgba(99,102,241,0.3)`
- `.glass-card` — dark glass with backdrop-filter blur
- `.custom-scrollbar` — 4px wide scrollbar
- `.reveal` / `.reveal-d1/d2/d3` — IntersectionObserver scroll reveal
- `.hero-item` / `.hero-d1/d2/d3/d4` — page stagger animations
- `.animate-float` — floating Y-axis keyframe animation
- `.animate-modal` — spring scale-in for modals

## Database Migrations
- accounts: 0001_initial → 0006_giftcode
- analytics_app: 0001_initial (ProfileView, LinkClick)

## Rate Limiting
| Endpoint | Limit | Key | Library |
|----------|-------|-----|---------|
| `redeem_gift_code` | 5/hour | user | django-ratelimit |
| `avatar_upload` | 20/hour | user | django-ratelimit |
| `background_upload` | 20/hour | user | django-ratelimit |
| Login URLs | 20/minute | IP | Custom middleware |

## Dev Setup Notes
- Run: `python manage.py runserver`
- Dev login: visit `/dev-login/` (no Google OAuth needed)
- testuser: Standard plan until 2027-06-16
- pip: use `python -m pip install` (not bare `pip` on this machine)
- Test gift code: `TEST-2026-FREE`
- Dev profile: `http://127.0.0.1:8000/@testuser/`
- Analytics: `http://127.0.0.1:8000/dashboard/analytics/`

## Technical Constraints
- File uploads: avatar 2MB, bg image 8MB
- Free plan: 2 links max, Standard: 10 links max
- Username: `^[a-z0-9_\-]{3,30}$` regex enforced client + server
- Gift codes: max 10 per generate action; uniqueness collision-safe
- Analytics: IP stored as SHA256 hash (first 32 chars), never raw
- qr-code-styling.js: Standard plan only (script inside {% if profile.is_standard %})

## Dependencies (requirements.txt)
```
Django==5.2.15
django-allauth==65.18.0
django-ratelimit==4.1.0
Pillow==12.1.1
qrcode==8.2
PyJWT (allauth dep)
```
