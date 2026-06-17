# Active Context — taplink.my

## Current Status
**Phase: Active Development — Dashboard fully functional, refining UX**

Django project is running. All core models migrated. Dev login bypass active (`/dev-login/`). testuser has Standard plan for testing.

## What Was Just Built (2026-06-16, Session 2)

### Bug fixes
- Per-link color not reflecting in preview → fixed `previewBtnStyle()` to use `link.color` instead of global `btn.color`
- Color picker `@change` → changed to `@input` for live preview on drag
- Hover animation toggle was wired but never applied → added `@mouseenter/@mouseleave` with `translateY(-2px)` to preview links

### Link model expanded (3 new fields, all migrated)
- `text_color` (#ffffff default) — label text color per link
- `icon_color` (#ffffff default) — icon color per link, separate from text
- `font_family` (blank default) — per-link font; empty = use global/default

### Dashboard — Links tab changes
- Color row redesigned: 3 full-width swatch buttons (Button / Text / Icon), hidden color input behind label, clicking swatch opens native picker
- Font row added: horizontal scrollable list of font name buttons rendered in their own typeface
  - Free: Inter, Poppins, Kanit, Montserrat, Lato, Roboto Mono
  - Standard: Nunito (TikTok), Plus Jakarta Sans (Instagram), Roboto (YouTube), DM Sans (Twitter), Bebas Neue (Netflix), Fredoka (Snapchat), Playfair Display (Pinterest), Space Grotesk (Spotify), Outfit (LinkedIn), DM Mono (Discord)
  - Locked (greyed + lock icon) for Free users
- Free plan link limit removed (set to 9999) for dev testing
- "Add link" button no longer disabled/count shown as "X / 9999"

### Dashboard — Appearance tab changes
- Removed "Default button color" (global btn.color) — per-link color is source of truth
- Removed entire Typography accordion section — font is now per-link only
- "Hover animation" toggle remains in Buttons section — working
- "Plain" button style added (no bg, no border — text only)

### Dashboard — Settings tab changes
- Removed Profile information card (display name, bio, location, birth year) — duplicated Appearance
- Added Username card:
  - Shows current URL: `taplink.my/username`
  - New username input with prefix `taplink.my/` visible inline
  - Debounced (400ms) live availability check via `accounts:check_username`
  - Green ✓ / red ✗ status icon in input field
  - "Change username" button disabled until available
  - Confirmation modal: shows old URL struck through, new URL green; requires typing current username to confirm
  - On success: state updates without page reload
- New view: `dashboard:username_change` (POST, validates regex + banned list + uniqueness)

### Preview panel
- Icon color: `link.icon_color`
- Text color: `link.text_color`
- Font: `link.font_family || font.family` (per-link or global fallback)
- Button style: uses `link.color` as the per-link color for all styles (filled, outline, soft, shadow, gradient, plain)
- Hover animation: CSS transition `translateY(-2px)` on mouseenter when `btn.hover` is true

## Current State of Models

### Link model fields
```python
user, title, url, icon, icon_type, color, text_color, icon_color, font_family,
display_style, thumbnail_url, is_active, order, created_at
```

### Appearance model fields (unchanged)
```python
user, avatar_shape, border_color, border_width,
bg_type, bg_color, bg_color2, bg_gradient_dir, bg_image, bg_video_url,
btn_style, btn_color, btn_text_color, btn_radius, btn_hover,
font_family, font_size, text_color,
social_icon_style, social_icon_size
```
Note: `btn_color`, `font_family`, `font_size`, `text_color` in Appearance are no longer shown in the UI but remain in the DB for now.

## Next Steps
1. Page 8: Public profile page (subdomain routing — `username.taplink.my`)
2. Page 9: Upgrade page
3. Page 10: QR Code page
4. Page 11: Admin panel

## Active Decisions
- **Per-link appearance** is the design philosophy: each link controls its own color, text color, icon color, font
- **Global Appearance** is for background, button style/radius/hover, avatar/profile section only
- **Free plan link limit** temporarily set to 9999 for dev — will restore to 2 before launch
- **testuser** has Standard plan, expires 2027-06-16
- **Dev login** at `/dev-login/` — active in DEBUG only
