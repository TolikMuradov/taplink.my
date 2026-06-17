# Tech Context — taplink.my

## Core Technologies

### Backend
- **Django 5.x** — Main framework
- **django-allauth** — Google OAuth (`SOCIALACCOUNT_ONLY = True`, `ACCOUNT_SIGNUP_FIELDS = []`)
- **PyJWT** — Required by allauth (installed)
- **Python 3.10** (Windows, `python` in PATH)

### Frontend
- **Django Templates** — Server-side rendering
- **TailwindCSS v3 CDN** — `https://cdn.tailwindcss.com?plugins=forms,container-queries`
- **Alpine.js v3 CDN** — `https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js`
- **Alpine Collapse plugin** — loaded BEFORE Alpine
- **Material Symbols Outlined** — Google Fonts icon font
- **Inter** — Primary font (loaded in base.html)
- **Platform fonts** — Loaded in dashboard `extra_head` block
- **Public profile** — Standalone HTML (no base.html), minimal JS, Tailwind NOT used (inline styles)

### Infrastructure
- **SQLite** (dev) — `db.sqlite3` in project root
- **Caddy** — Planned for prod (wildcard SSL `*.taplink.my`)
- No build pipeline — CDN only for now

### Authentication
- Google OAuth 2.0 only via allauth
- Adapter: `accounts.adapters.TaplinkSocialAccountAdapter`

## Project Structure (actual)
```
config/
  settings.py   — Main settings
  urls.py       — Root URL config
  wsgi.py / asgi.py
core/
  urls.py       — landing, upgrade, upgrade/redeem, privacy, terms, dev-login
  views.py      — landing, upgrade, redeem_gift_code, privacy, terms, dev_login
accounts/
  models.py     — UserProfile, Link, Appearance, GiftCode + signals
  adapters.py   — TaplinkSocialAccountAdapter
  admin.py      — All models registered; GiftCodeAdmin with generate view
  views.py      — onboarding, check_username
  urls.py       — onboarding/, check-username/
  migrations/   — 0001..0006 (latest: giftcode)
dashboard/
  views.py      — home, link CRUD, appearance, settings, username_change, account_delete
  urls.py       — 9 URL patterns
profiles/
  views.py      — public_profile, link_redirect
  urls.py       — /@<username>/, /@<username>/r/<link_id>/
  middleware.py — SubdomainMiddleware
analytics_app/  — stub (models, views empty)
templates/
  base.html               — Indigo Dark design system, Alpine, Tailwind config
  core/landing.html
  core/upgrade.html       — Upgrade page with gift code UI
  core/privacy.html
  core/terms.html
  account/login.html
  accounts/onboarding.html
  dashboard/home.html     — 1300+ lines, full dashboard SPA
  profiles/public_profile.html — Standalone public profile (no base.html)
  profiles/not_found.html
  profiles/paused.html
  admin/accounts/giftcode/generate.html — Custom admin generate page
  admin/accounts/giftcode/change_list.html — Adds "Generate" button to changelist
memory-bank/    — This documentation system
```

## Indigo Dark Design System (in base.html tailwind.config)
Key color tokens:
- `primary: #c0c1ff`, `on-primary: #1000a9`
- `primary-container: #8083ff`
- `background: #13131b`, `surface: #13131b`
- `surface-container: #1f1f27`, `surface-container-high: #292932`
- `outline-variant: #464554`
- `error: #ffb4ab`, `tertiary: #ffb783`

Key CSS classes:
- `.brand-glow` — `box-shadow: 0 0 20px rgba(99,102,241,0.3)`
- `.glass-card` — `background: rgba(27,27,35,0.8); backdrop-filter: blur(12px); border: 1px solid rgba(144,143,160,0.2)`
- `.custom-scrollbar` — 4px wide scrollbar

## Database Migrations (accounts app)
- 0001_initial — UserProfile, Link, Appearance
- 0002 — earlier fix
- 0003_link_text_color — added `text_color` to Link
- 0004_link_icon_color — added `icon_color` to Link
- 0005_link_font_family — added `font_family` to Link
- 0006_giftcode — added GiftCode model

## Dev Setup Notes
- Run: `python manage.py runserver`
- Dev login: visit `/dev-login/` (no Google OAuth needed)
- testuser credentials: `testuser` / `test1234`, Standard plan until 2027-06-16
- pip: use `python -m pip install` (not bare `pip` on this machine)
- Test gift code: `TEST-2026-FREE`
- Dev profile URL: `http://127.0.0.1:8000/@testuser/`

## Technical Constraints
- File uploads: avatar 2MB, bg image 5MB, bg video 30MB (Standard only)
- Rate limiting: 10 req/min on login (not yet implemented)
- Username: `^[a-z0-9_\-]{3,30}$` regex enforced client + server side
- Gift codes: max 10 per generate action; uniqueness collision-safe

## Dependencies Installed
```
django
django-allauth
Pillow
PyJWT
```
Still needed:
```
qrcode[pil]     # QR generation (Page 7)
django-ratelimit # rate limiting
```
