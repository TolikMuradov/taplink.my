# Progress — taplink.my

## Current Status: Active Development

## What Works ✅

### Foundation
- [x] Django project initialized (`config/` settings, `manage.py`)
- [x] App structure: `core`, `accounts`, `dashboard` (profiles/analytics/admin_panel stubs)
- [x] Dependencies installed: django-allauth, Pillow, PyJWT, etc.
- [x] Settings: DB (SQLite dev), allauth (SOCIALACCOUNT_ONLY=True), MEDIA_ROOT, STATIC_ROOT
- [x] TailwindCSS CDN + Alpine.js CDN (no build pipeline needed for now)
- [x] Dev login bypass: `/dev-login/` → authenticates testuser, DEBUG only

### Design System
- [x] Indigo Dark design system in `base.html`: full color token set, typography scale, spacing, glassmorphism
- [x] Material Symbols Outlined icons throughout
- [x] `showToast()` global function
- [x] `[x-cloak]` handled

### Database Models (all migrated)
- [x] UserProfile (username, display_name, bio, location, birth_year, avatar, plan, plan_expires, is_paused, onboarded, marketing, seo_title, seo_description)
- [x] Link (title, url, icon, icon_type, **color, text_color, icon_color, font_family**, display_style, thumbnail_url, is_active, order)
- [x] Appearance (avatar_shape, border_color/width, bg_*, btn_*, font_*, social_icon_*)
- [ ] Analytics model
- [ ] GiftCode model
- [ ] Announcement model

### Auth & Onboarding
- [x] Google OAuth via django-allauth
- [x] `TaplinkSocialAccountAdapter` → new users → onboarding, existing → dashboard
- [x] Onboarding: 2-step modal (profiling + username), debounced AJAX availability check
- [x] Banned username list

### Pages
- [x] Page 1: Landing page (interactive Alpine demo, features, pricing)
- [x] Page 2: Login (glass-card, Google OAuth button)
- [x] Page 3: Onboarding modal
- [x] Page 4: Dashboard — Links tab
  - CRUD (add/edit/delete), drag handle, active toggle
  - Icon picker (29 icons, 6 categories, searchable)
  - Per-link: color (button bg), text_color, icon_color — swatch pickers
  - Per-link font: scrollable selector, own typeface preview
  - Free fonts: Inter, Poppins, Kanit, Montserrat, Lato, Roboto Mono
  - Standard fonts: Nunito, Plus Jakarta Sans, Roboto, DM Sans, Bebas Neue, Fredoka, Playfair Display, Space Grotesk, Outfit, DM Mono (locked + greyed for Free)
- [x] Page 5: Dashboard — Appearance tab
  - Profile accordion: avatar shape, border color/width, display name, bio, location
  - Background accordion: color/gradient/image/video (image+video Standard only)
  - Buttons accordion: style (filled/outline/soft/shadow/glass/gradient/plain), text color, corner radius, hover animation toggle
  - Typography accordion: REMOVED (now per-link)
  - Sticky Save button
- [x] Page 6: Dashboard — Analytics tab (locked state for Free, 4 stat cards for Standard)
- [x] Page 7: Dashboard — Settings tab
  - Username card: current URL display, new username input with live check, confirmation modal (requires typing current username)
  - SEO card: title + description with char counters
  - Visibility: pause toggle
  - Custom domain: coming soon placeholder
  - Email preferences: marketing toggle
  - Account: email display + delete account modal
- [ ] Page 8: Public profile (subdomain)
- [ ] Page 9: Upgrade page
- [ ] Page 10: QR Code page
- [ ] Page 11: Admin panel

### Dashboard — Right Preview Panel
- [x] Phone mockup showing live reactive preview
- [x] Avatar, display name, bio, location
- [x] Links with per-link: button style, color, text_color, icon_color, font_family
- [x] Hover animation (translateY lift when btn.hover = true)
- [x] Watermark for Free plan
- [x] Copy link + open page buttons

### Features
- [x] Google OAuth flow + new user detection
- [x] Username availability check (real-time AJAX, debounced)
- [x] Username change (Settings → modal → API, live state update)
- [x] Icon picker (searchable, 6 categories)
- [x] Toast notification system
- [x] Per-link color / text color / icon color pickers
- [x] Per-link font selector (Free + Standard tiers)
- [x] Button styles: filled, outline, soft, shadow, glass, gradient, plain
- [x] Hover animation toggle
- [x] Drag handle (UI ready, reorder API exists)
- [x] Free plan watermark (UI)
- [ ] Drag-and-drop reorder (JS SortableJS not wired yet)
- [ ] Avatar upload + cropping
- [ ] Background image/video upload
- [ ] QR code generator
- [ ] Analytics tracking (view + click events)
- [ ] Analytics charts
- [ ] Gift code redemption
- [ ] SEO meta tags on public profile
- [ ] Rate limiting on login
- [ ] Splash screen redirect (Standard plan)

### Admin Panel
- [ ] All sections (not started)

## Known Issues / Dev Notes
- Free plan limit set to 9999 (unlimited) for dev — restore to 2 before launch
- testuser has Standard plan until 2027-06-16
- `btn_color`, `font_family`, `font_size`, `text_color` still in Appearance DB but not shown in UI
- Drag-and-drop: handle exists, `link_reorder` API exists, but SortableJS not wired to DOM

## Evolution of Decisions
- 2026-06-16 (Session 1): Project initialized, Indigo Dark design applied, Pages 1-7 implemented
- 2026-06-16 (Session 2):
  - Per-link appearance model: each link has own color, text_color, icon_color, font_family
  - Global "default button color" removed from Appearance (per-link color is source of truth)
  - Typography accordion removed from Appearance (font now per-link only)
  - Settings profile fields removed (duplicated Appearance; username change added instead)
  - Button styles expanded with "plain" (text only, no bg/border)
  - Free plan fonts: 6 basics; Standard: 10 platform-inspired fonts
