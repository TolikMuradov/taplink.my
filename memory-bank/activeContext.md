# Active Context — taplink.my

## Current Status
**Phase: Active Development — Pages 1-6 complete, Pages 7-8 remaining**

Django project is running. All core models migrated. Dev login bypass active (`/dev-login/`). testuser has Standard plan for testing.

## What Was Just Built (2026-06-17, Session 3)

### Sayfa 5 — Upgrade (`/upgrade/`)
- `GiftCode` model added to `accounts/models.py` (code, plan, duration_days, is_used, used_by, used_at)
- Migration `0006_giftcode` applied
- `/upgrade/` view: 3 hover-reveal feature cards, comparison table, gift code input, PromptPay placeholder
- `/upgrade/redeem/` AJAX endpoint: validates code, activates Standard, extends expiry if already Standard
- Dashboard sidebar "Upgrade" button wired to `/upgrade/`
- GiftCode registered in Django admin with custom generator

### Gift Code Generator (Django Admin)
- `/admin/accounts/giftcode/generate/` — custom admin view
- Format: `XXXX-XXXX-XXXX` (12 chars, no ambiguous 0/O/1/I/L)
- Generate 1 / 5 / 10 codes per click
- Configurable duration (default 30 days, max 365)
- Copy individual or all codes to clipboard
- Test code: `TEST-2026-FREE` (pre-seeded)

### Sayfa 6 — Public Profile (`/@username/` dev, `username.taplink.my` prod)
- `profiles/views.py`: `public_profile()` + `link_redirect()` (analytics hook)
- `profiles/urls.py`: `/@<username>/` and `/@<username>/r/<link_id>/`
- `profiles/middleware.py`: `SubdomainMiddleware` — detects `username.taplink.my` host, routes to profile view
- `config/settings.py`: SubdomainMiddleware added, `.localhost` added to ALLOWED_HOSTS
- Full appearance rendering: bg color/gradient/image/video, avatar shape (circle/square/hexagon) + border
- Per-link button styles computed in view (`_build_btn_css`) → passed as inline CSS
- `icon_only` links → compact social icon row (top), `icon_text` links → full button list
- Standard: ripple effect + 0.5s splash screen on click; Free: direct window.open + watermark
- SEO: `<title>`, meta description, Open Graph tags, JSON-LD Person schema
- Error pages: `not_found.html` (404), `paused.html` (is_paused=True)

## Current State of Models

### accounts app models
- `UserProfile`: username, display_name, bio, location, birth_year, avatar, plan, plan_expires, is_paused, onboarded, marketing, seo_title, seo_description
- `Link`: user, title, url, icon, icon_type, color, text_color, icon_color, font_family, display_style, thumbnail_url, is_active, order
- `Appearance`: avatar_shape, border_color/width, bg_*, btn_*, font_*, social_icon_*
- `GiftCode`: code, plan, duration_days, is_used, used_by, used_at, created_at

### Migrations (accounts)
0001_initial → 0002 → 0003_link_text_color → 0004_link_icon_color → 0005_link_font_family → 0006_giftcode

## Next Steps
1. **Page 7: QR Code** (`/dashboard/qr/`) — Free: B&W QR + download; Standard: color/logo/style editor
2. **Page 8: Admin Panel** (`/admin-panel/`) — custom admin UI (not Django admin), superuser only

## Active Decisions
- **Per-link appearance** is the design philosophy: each link controls its own color, text_color, icon_color, font
- **Global Appearance** is for background, button style/radius/hover, avatar/profile section only
- **Free plan link limit** temporarily set to 9999 for dev — will restore to 2 before launch
- **testuser** has Standard plan, expires 2027-06-16
- **Dev login** at `/dev-login/` — active in DEBUG only
- **Subdomain routing**: `SubdomainMiddleware` for prod; `/@username/` path for dev testing
- **Platform icons**: `icon_type='material'` → Material Symbols; platform name → colored initial badge (SVGs to be added later)
- **Settings tab** has username change (not in original plan.txt) — deliberate addition
- **Typography in Appearance** removed — font is per-link only
