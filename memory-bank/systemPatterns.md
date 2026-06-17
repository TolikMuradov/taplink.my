# System Patterns — taplink.my

## Architecture Overview

```
taplink.my (main domain)
├── /                    — Landing page (core)
├── /accounts/login/     — Google OAuth (allauth)
├── /accounts/onboarding/ — 2-step modal (accounts)
├── /dashboard/          — Editor (dashboard)
├── /upgrade/            — Upgrade page (core)
├── /upgrade/redeem/     — Gift code AJAX endpoint (core)
├── /@<username>/        — Public profile DEV route (profiles)
├── /@<username>/r/<id>/ — Link redirect / analytics hook (profiles)
├── /admin/              — Django admin (superuser)
├── /admin/accounts/giftcode/generate/ — Gift code generator
└── /dev-login/          — DEBUG-only bypass (core)

username.taplink.my (wildcard subdomain)
└── /  — Public profile via SubdomainMiddleware → profiles.views.public_profile
```

## URL Structure (config/urls.py)
```python
path('admin/', admin.site.urls)
path('accounts/', include('allauth.urls'))
path('accounts/', include('accounts.urls'))   # onboarding, check_username
path('dashboard/', include('dashboard.urls')) # home, link CRUD, appearance, settings
path('', include('profiles.urls'))            # /@username/ dev routes
path('', include('core.urls'))                # landing, upgrade, privacy, terms, dev-login
```

## Auth Flow
- **Google OAuth only** via django-allauth (`SOCIALACCOUNT_ONLY = True`)
- `TaplinkSocialAccountAdapter.get_login_redirect_url()`:
  - `profile.onboarded = False` → `/accounts/onboarding/`
  - Otherwise → `/dashboard/`
- **Dev bypass:** `/dev-login/` logs in `testuser`/`test1234`, DEBUG only

## Subdomain Routing
```
SubdomainMiddleware (profiles/middleware.py)
├── Detects HTTP_HOST ending in .taplink.my
├── Extracts subdomain (username)
├── Skips reserved subdomains (www, api, admin, dashboard, etc.)
└── Calls profiles.views.public_profile(request, username=subdomain)
```
Dev testing: `http://127.0.0.1:8000/@testuser/`
Prod: `http://testuser.taplink.my/` (Caddy wildcard SSL)

## Dashboard Architecture

### Alpine.js `dashboardApp()` state tree
```
activeTab: 'links' | 'appearance' | 'analytics' | 'settings'
isStandard: bool
links: INITIAL_LINKS[]  (each: id, title, url, icon, color, text_color, icon_color, font_family, is_active, order)
profile: { displayName, bio, location, avatar }
bg: { type, color, color2, dir }
btn: { style, textColor, radius, hover }
font: { family, size, textColor }  (global fallback — font now per-link)
appearance: { avatar_shape, border_color, border_width }
settings: { username, newUsername, usernameStatus, usernameError, usernameConfirm, seoTitle, seoDescription, isPaused, marketing }
showDeleteModal, showUsernameModal, showIconPicker, iconPickerLinkId
```

### AJAX Endpoints (dashboard app)
| URL | Method | Purpose |
|-----|--------|---------|
| `links/create/` | POST | Create link |
| `links/<pk>/update/` | POST | Update link fields |
| `links/<pk>/delete/` | POST | Delete link |
| `links/reorder/` | POST | Update link order |
| `appearance/save/` | POST | Save all appearance fields |
| `settings/save/` | POST | Save SEO, pause, marketing |
| `settings/username/` | POST | Change username |
| `account/delete/` | POST | Delete account |

### AJAX Endpoints (core app)
| URL | Method | Purpose |
|-----|--------|---------|
| `upgrade/redeem/` | POST | Validate + activate gift code |

### AJAX Endpoints (accounts app)
| URL | Method | Purpose |
|-----|--------|---------|
| `accounts/check-username/` | GET | Username availability check |

## Public Profile — Button Style Logic
```python
# profiles/views.py → _build_btn_css(link, appearance)
c = link.color or '#8083ff'
t = link.text_color or '#ffffff'

filled   → background:c; color:t;
outline  → background:transparent; color:c; border:2px solid c;
soft     → background:c33; color:c;
shadow   → background:c; color:t; box-shadow:0 4px 20px c66;
glass    → background:rgba(255,255,255,0.12); backdrop-filter:blur(10px);
gradient → background:linear-gradient(135deg,c,c99); color:t;
plain    → background:transparent; color:c;
```

### Dashboard Preview — same logic in JS (`previewBtnStyle`)
```js
const c = link.color || '#8083ff';
switch(btn.style): filled/outline/soft/shadow/glass/gradient/plain
```

## Plan-gated Features
| Feature | Free | Standard |
|---------|------|----------|
| Links | 2 (unlimited in dev) | 10 |
| Analytics tab | Locked | Unlocked |
| Background image/video | ✗ | ✓ |
| Platform fonts (Nunito etc.) | Locked | Unlocked |
| Watermark on public profile | ✓ | ✗ |
| Splash screen redirect | ✗ | ✓ (ripple + 0.5s splash) |
| Custom QR | ✗ | ✓ |

## Gift Code System
```
GiftCode model (accounts/models.py)
├── code: unique XXXX-XXXX-XXXX format
├── plan: 'standard'
├── duration_days: 30 (default)
├── is_used / used_by / used_at
└── created_at

Generator: /admin/accounts/giftcode/generate/
  ├── 1 / 5 / 10 codes per click
  ├── Configurable duration (default 30d)
  └── Uniqueness guaranteed (collision retry)

Redemption: POST /upgrade/redeem/
  ├── Validates code exists + not used
  ├── Extends expiry if already Standard
  └── Activates Standard plan
```

## Font System
- **Free fonts:** Inter, Poppins, Kanit, Montserrat, Lato, Roboto Mono
- **Standard fonts:** Nunito (TikTok), Plus Jakarta Sans (Instagram), Roboto (YouTube), DM Sans (Twitter/X), Bebas Neue (Netflix), Fredoka (Snapchat), Playfair Display (Pinterest), Space Grotesk (Spotify), Outfit (LinkedIn), DM Mono (Discord)
- Per-link: `link.font_family` field; empty = global fallback
- Public profile: collects unique fonts, builds single Google Fonts URL

## Auto-save Pattern
- Text inputs: `@change="updateLink(link)"` (on blur)
- Color pickers: `@input="updateLink(link)"` (live, on drag)
- Font/icon selections: immediate AJAX call
- Appearance: explicit Save button (`saveAppearance()`)
- Settings: explicit Save button or immediate for toggles

## Username Change Flow
1. User types new username → debounced 400ms → `check_username` AJAX
2. Status: checking → available / taken / invalid
3. "Change username" button enabled only when `status === 'available'`
4. Modal: shows old URL struck through + new URL green
5. User types current username to confirm → "Confirm" button enabled
6. POST to `dashboard:username_change` → validates server-side
7. On success: Alpine state updates, modal closes, toast shown

## Security Patterns
- CSRF on all POST requests (`X-CSRFToken` header from `CSRF_TOKEN` JS var)
- User ownership checked on every link/appearance action
- Username: regex `^[a-z0-9_\-]{3,30}$` + banned list + uniqueness
- Gift codes: uniqueness enforced at DB level (unique=True) + collision retry
- `dev_login` raises Http404 when `DEBUG = False`
- SubdomainMiddleware skips reserved subdomains
