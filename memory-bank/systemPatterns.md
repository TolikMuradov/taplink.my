# System Patterns — taplink.my

## Architecture Overview

```
taplink.my (main domain)
├── /                  — Landing page (core)
├── /accounts/login/   — Google OAuth (allauth)
├── /accounts/onboarding/ — 2-step modal (accounts)
├── /dashboard/        — Editor (dashboard)
├── /dev-login/        — DEBUG-only bypass (core)
└── /admin/            — Django admin (superuser)

username.taplink.my (wildcard subdomain) — NOT YET BUILT
└── /                  — Public profile page
```

## URL Structure (implemented)
```python
# config/urls.py
path('admin/', admin.site.urls)
path('accounts/', include('allauth.urls'))
path('accounts/', include('accounts.urls'))   # onboarding, check_username
path('dashboard/', include('dashboard.urls')) # home, link CRUD, appearance, settings
path('', include('core.urls'))                # landing, privacy, terms, dev-login
```

## Auth Flow
- **Google OAuth only** via django-allauth (`SOCIALACCOUNT_ONLY = True`)
- `TaplinkSocialAccountAdapter.get_login_redirect_url()`:
  - `profile.onboarded = False` → `/accounts/onboarding/`
  - Otherwise → `/dashboard/`
- **Dev bypass:** `/dev-login/` logs in `testuser`/`test1234`, DEBUG only

## Dashboard Architecture

### Alpine.js `dashboardApp()` state tree
```
activeTab: 'links' | 'appearance' | 'analytics' | 'settings'
isStandard: bool  (from Django template context)
links: INITIAL_LINKS[]  (each: id, title, url, icon, color, text_color, icon_color, font_family, is_active, order)
profile: { displayName, bio, location, avatar }
bg: { type, color, color2, dir }
btn: { style, textColor, radius, hover }
font: { family, size, textColor }  (global fallback only — font now per-link)
appearance: { avatar_shape, border_color, border_width }
settings: { username, newUsername, usernameStatus, usernameError, usernameConfirm, seoTitle, seoDescription, isPaused, marketing }
showDeleteModal: bool
showUsernameModal: bool
showIconPicker: bool
iconPickerLinkId: int | null
```

### AJAX Endpoints (dashboard app)
| URL | Method | Purpose |
|-----|--------|---------|
| `links/create/` | POST | Create link (returns full link object) |
| `links/<pk>/update/` | POST | Update link fields (color, text_color, icon_color, font_family, etc.) |
| `links/<pk>/delete/` | POST | Delete link |
| `links/reorder/` | POST | Update link order |
| `appearance/save/` | POST | Save all appearance fields |
| `settings/save/` | POST | Save SEO, pause, marketing |
| `settings/username/` | POST | Change username (validates + updates) |
| `account/delete/` | POST | Delete account |

### Per-link Appearance Design
Each `Link` has independent:
- `color` — button background / accent color
- `text_color` — label text color
- `icon_color` — icon color
- `font_family` — font (empty = fallback to global)

Global `Appearance` controls: background, button style/radius/hover, avatar shape/border.

### Preview Panel — `previewBtnStyle(link)` logic
```js
const c = link.color || '#8083ff';
switch(btn.style):
  filled   → background: c
  outline  → border: 1.5px solid c
  soft     → background: c + '33'
  shadow   → background: c + box-shadow: c + '66'
  glass    → rgba white background + blur
  gradient → linear-gradient(135deg, c, c + '99')
  plain    → transparent
```

Icon color: `link.icon_color`
Text color: `link.text_color`
Font: `link.font_family || font.family`
Hover: `@mouseenter → translateY(-2px)` when `btn.hover === true`

## Plan-gated Features
| Feature | Free | Standard |
|---------|------|----------|
| Links | 2 (unlimited in dev) | 10 |
| Analytics tab | Locked | Unlocked |
| Background image/video | ✗ | ✓ |
| Platform fonts (Nunito etc.) | Locked | Unlocked |
| Watermark on public profile | ✓ | ✗ |
| Splash screen redirect | ✗ | ✓ |
| Custom QR | ✗ | ✓ |

## Font System
- **Free fonts:** Inter, Poppins, Kanit, Montserrat, Lato, Roboto Mono
- **Standard fonts:** Nunito (TikTok), Plus Jakarta Sans (Instagram), Roboto (YouTube), DM Sans (Twitter/X), Bebas Neue (Netflix), Fredoka (Snapchat), Playfair Display (Pinterest), Space Grotesk (Spotify), Outfit (LinkedIn), DM Mono (Discord)
- Loaded via Google Fonts in dashboard `extra_head` block
- Displayed in their own typeface in the selector
- Per-link: `link.font_family` field; empty = global fallback

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
4. Modal opens: shows old URL (struck through) + new URL (green)
5. User types current username to confirm → "Confirm" button enabled
6. POST to `dashboard:username_change` → validates again server-side
7. On success: Alpine state updates username, modal closes, toast shown

## Security Patterns
- CSRF on all POST requests (`X-CSRFToken` header from `CSRF_TOKEN` JS var)
- User ownership checked on every link/appearance action
- Username: regex `^[a-z0-9_\-]{3,30}$` + banned list + uniqueness
- `dev_login` raises Http404 when `DEBUG = False`
