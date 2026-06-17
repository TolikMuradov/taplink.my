# Progress — taplink.my

## Current Status: Active Development

## What Works ✅

### Foundation
- [x] Django project initialized (`config/` settings, `manage.py`)
- [x] App structure: `core`, `accounts`, `dashboard`, `profiles`, `analytics_app` (stub)
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
- [x] Link (title, url, icon, icon_type, color, text_color, icon_color, font_family, display_style, thumbnail_url, is_active, order)
- [x] Appearance (avatar_shape, border_color/width, bg_*, btn_*, font_*, social_icon_*)
- [x] GiftCode (code, plan, duration_days, is_used, used_by, used_at, created_at)
- [ ] Analytics model (PageView, LinkClick)
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
  - Standard fonts: Nunito, Plus Jakarta Sans, Roboto, DM Sans, Bebas Neue, Fredoka, Playfair Display, Space Grotesk, Outfit, DM Mono (locked for Free)
- [x] Page 4: Dashboard — Appearance tab
  - Profile accordion: avatar shape, border color/width, display name, bio, location
  - Background accordion: color/gradient/image/video (image+video Standard only)
  - Buttons accordion: style (filled/outline/soft/shadow/glass/gradient/plain), text color, corner radius, hover toggle
  - Sticky Save button
- [x] Page 4: Dashboard — Analytics tab (locked state for Free, 4 stat cards for Standard)
- [x] Page 4: Dashboard — Settings tab
  - Username card: current URL display, new username input with live check, confirmation modal
  - SEO card: title + description with char counters
  - Visibility: pause toggle
  - Custom domain: coming soon placeholder
  - Email preferences: marketing toggle
  - Account: email display + delete account modal
- [x] Page 5: Upgrade page (`/upgrade/`)
  - 3 hover-reveal feature cards (Full Customization, Analytics, Custom QR)
  - Plan comparison table
  - Gift code input + AJAX redemption endpoint
  - PromptPay placeholder (Coming soon)
  - Sidebar Upgrade button wired
- [x] Page 6: Public Profile (`/@username/` dev, `username.taplink.my` prod)
  - SubdomainMiddleware for prod routing
  - Full appearance rendering (bg, avatar, buttons, fonts)
  - Social icons row (icon_only) + main link buttons (icon_text)
  - Standard: ripple + splash screen; Free: direct redirect + watermark
  - SEO: title, OG tags, JSON-LD
  - 404 + paused error pages
- [ ] Page 7: QR Code (`/dashboard/qr/`)
- [ ] Page 8: Admin Panel (`/admin-panel/`)

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
- [x] Gift code generation (admin) + redemption (upgrade page)
- [x] Drag handle (UI ready, reorder API exists)
- [ ] Drag-and-drop reorder (SortableJS not wired yet)
- [ ] Avatar upload + cropping
- [ ] Background image/video upload
- [ ] QR code generator
- [ ] Analytics tracking (view + click events)
- [ ] Analytics charts
- [ ] SEO meta tags applied on public profile ✅ (done in Page 6)
- [ ] Rate limiting on login
- [ ] Splash screen redirect ✅ (done in Page 6)

### Admin
- [x] Django admin: UserProfile, Link, Appearance, GiftCode registered
- [x] Gift code generator at `/admin/accounts/giftcode/generate/`
- [ ] Custom admin panel (Page 8: `/admin-panel/`)

## Known Issues / Dev Notes
- Free plan limit set to 9999 (unlimited) for dev — restore to 2 before launch
- testuser has Standard plan until 2027-06-16
- `btn_color`, `font_family`, `font_size`, `text_color` still in Appearance DB but not shown in UI
- Drag-and-drop: handle exists, `link_reorder` API exists, but SortableJS not wired to DOM
- Platform brand icons rendered as initial-letter badges — real SVGs to be added later
- `qrcode` pip package not yet installed (needed for Page 7)

## Evolution of Decisions
- 2026-06-16 (Session 1): Project initialized, Indigo Dark design applied, Pages 1-4 (dashboard) implemented
- 2026-06-16 (Session 2): Per-link appearance model, font system, username change feature, "plain" button style
- 2026-06-17 (Session 3): Pages 5-6, GiftCode model, upgrade page, gift code generator, public profile with subdomain routing
