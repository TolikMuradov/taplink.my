# Active Context — taplink.my

## Current Status
**Phase: Active Development — Pages 1-7 complete, Page 8 (Admin Panel) remaining**

## What Was Built (2026-06-17, Session 3)

### Page 5 — Upgrade (`/upgrade/`)
- GiftCode model + migration 0006
- 3 hover-reveal feature cards, comparison table, gift code input, PromptPay placeholder
- `/upgrade/redeem/` AJAX endpoint — validates, activates/extends Standard
- Dashboard sidebar Upgrade button wired

### Gift Code Generator (Django Admin)
- `/admin/accounts/giftcode/generate/` custom admin view
- Format: `XXXX-XXXX-XXXX` (no ambiguous chars), 1/5/10 per click, default 30 days
- Test code: `TEST-2026-FREE`

### Page 6 — Public Profile (`/@username/` dev, `username.taplink.my` prod)
- `profiles/views.py`: public_profile + link_redirect
- `profiles/middleware.py`: SubdomainMiddleware
- Full appearance: bg color/gradient/image/video, avatar shape + border
- `icon_only` links → social icon row; `icon_text` → full button list
- Standard: ripple + 0.5s splash screen; Free: direct redirect + watermark
- SEO: title, OG tags, JSON-LD; 404 + paused pages

### Page 7 — QR Code (`/dashboard/qr/`)
- `qrcode[pil]` already installed (Pillow + qrcode packages present)
- Free: B&W QR, PNG download, upgrade banner
- Standard: live editor (350ms debounce AJAX preview)
  - Color pickers (fg/bg), corner styles (square/rounded/dot via StyledPilImage)
  - Logo: none / taplink.my / upload own (base64)
  - Logo size slider (10-35%), padding slider (1-8)
  - PNG (512×512) + SVG download
- `/dashboard/qr/preview/` — POST, returns base64 PNG
- `/dashboard/qr/download/` — GET, serves file
- QR link added to dashboard sidebar
- **Fix**: import was `colormask` → correct is `colormasks` (plural)

### UX Fixes (same session)
- Hexagon avatar shape removed — only circle + square remain
- Font picker redesigned: compact single-line display → click → 3-col grid panel
  - Free section (Default + 6 fonts) + Standard section (10 fonts, locked for Free)
  - Alpine state: `openFontPicker: null` (link.id when open)

## Next Steps
1. **Page 8: Admin Panel** (`/admin-panel/`) — deferred, not priority yet
2. Drag & drop reorder (SortableJS — handle + API exist, not wired)
3. Avatar upload + crop
4. Background image/video upload
5. Analytics tracking + charts
6. Free plan link limit restore to 2 before launch

## Active Decisions
- Per-link appearance is the design philosophy
- testuser Standard plan until 2027-06-16, dev limit 9999 links
- SubdomainMiddleware for prod; `/@username/` path for dev
- colormasks import (plural) — qrcode library quirk
- Hexagon removed permanently — border CSS broken with clip-path
