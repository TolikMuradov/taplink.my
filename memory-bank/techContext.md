# Tech Context — taplink.my

## Core Technologies

### Backend
- **Django 5.x** — Main framework
- **django-allauth** — Google OAuth (`SOCIALACCOUNT_ONLY = True`, `ACCOUNT_SIGNUP_FIELDS = []`)
- **PyJWT** — Required by allauth (installed)
- **Python 3.10** (Windows, `python` or `python3` in PATH)

### Frontend
- **Django Templates** — Server-side rendering
- **TailwindCSS v3 CDN** — `https://cdn.tailwindcss.com?plugins=forms,container-queries`
- **Alpine.js v3 CDN** — `https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js`
- **Alpine Collapse plugin** — `https://unpkg.com/@alpinejs/collapse@3.x.x/dist/cdn.min.js` (loaded BEFORE Alpine)
- **Material Symbols Outlined** — Google Fonts icon font (not SVG, not Font Awesome)
- **Inter** — Primary font (loaded in base.html)
- **Platform fonts** — Loaded in dashboard `extra_head` block (Nunito, Plus Jakarta Sans, Roboto, DM Sans, Bebas Neue, Fredoka, Playfair Display, Space Grotesk, Outfit, DM Mono)

### Infrastructure
- **SQLite** (dev) — `db.sqlite3` in project root
- **Caddy** — Planned for prod (wildcard SSL `*.taplink.my`)
- No build pipeline — CDN only for now

### Authentication
- Google OAuth 2.0 only via allauth
- Settings: `SOCIALACCOUNT_ONLY = True`, `ACCOUNT_SIGNUP_FIELDS = []`
- Adapter: `accounts.adapters.TaplinkSocialAccountAdapter`

## Project Structure (actual)
```
config/
  settings.py   — Main settings (allauth, MEDIA, STATIC, TEMPLATES)
  urls.py       — Root URL config
core/
  urls.py       — landing, privacy, terms, dev-login
  views.py      — landing, privacy, terms, dev_login
accounts/
  models.py     — UserProfile, Link, Appearance + post_save signals
  adapters.py   — TaplinkSocialAccountAdapter
  views.py      — onboarding, check_username
  urls.py       — onboarding/, check-username/
  migrations/   — 0001..0005 (latest: link_font_family)
dashboard/
  views.py      — home, link_create, link_update, link_delete, link_reorder,
                  appearance_save, username_change, settings_save, account_delete
  urls.py       — 9 URL patterns
templates/
  base.html            — Indigo Dark design system, Alpine, Tailwind config
  core/landing.html
  account/login.html
  accounts/onboarding.html
  dashboard/home.html  — 1300+ lines, full dashboard SPA
memory-bank/           — This documentation system
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
- 0002_... — (earlier fix)
- 0003_link_text_color — added `text_color` to Link
- 0004_link_icon_color — added `icon_color` to Link
- 0005_link_font_family — added `font_family` to Link

## Dev Setup Notes
- Run: `python manage.py runserver`
- Dev login: visit `/dev-login/` (no Google OAuth needed)
- testuser credentials: `testuser` / `test1234`, Standard plan until 2027-06-16
- pip: use `python -m pip install` (not bare `pip` on this machine)

## Technical Constraints
- File uploads: avatar 2MB, bg image 5MB, bg video 30MB (Standard only)
- Rate limiting: 10 req/min on login (not yet implemented)
- Username: `^[a-z0-9_\-]{3,30}$` regex enforced client + server side

## Dependencies Installed
```
django
django-allauth
Pillow
PyJWT
```
Still needed:
```
qrcode          # QR generation
django-ratelimit # rate limiting
```
