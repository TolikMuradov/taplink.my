# Progress — taplink.my

## Current Status: Active Development — Pages 1-7 Done

## Pages ✅

- [x] Page 1: Landing page
- [x] Page 2: Login (Google OAuth)
- [x] Page 3: Onboarding modal
- [x] Page 4: Dashboard — Links, Appearance, Analytics (locked/unlocked), Settings tabs
- [x] Page 5: Upgrade page (`/upgrade/`) — gift code + PromptPay placeholder
- [x] Page 6: Public Profile (`/@username/` dev, `username.taplink.my` prod)
- [x] Page 7: QR Code (`/dashboard/qr/`) — Free B&W + Standard full editor
- [ ] Page 8: Admin Panel (`/admin-panel/`) — not started

## Models ✅ (all migrated)
- UserProfile, Link, Appearance, GiftCode
- migrations 0001→0006

## Key Features Status

### Done ✅
- Google OAuth + onboarding
- Dashboard 4-tab SPA (Alpine.js)
- Per-link color/text_color/icon_color/font_family
- 16 fonts (6 Free + 10 Standard), font picker dropdown grid
- Button styles: filled/outline/soft/shadow/glass/gradient/plain
- Avatar: circle + square (hexagon removed)
- SubdomainMiddleware (prod routing)
- Gift code system (model + generator in admin + redemption)
- QR: Free (B&W PNG) + Standard (colored/styled/logo, PNG+SVG)
- Public profile: full appearance, splash screen, watermark, SEO
- Django admin: all models + gift code generator

### Pending ❌
- Drag & drop reorder (handle+API exist, SortableJS not wired)
- Avatar upload + crop
- Background image/video upload
- Analytics model + tracking + charts
- Rate limiting on login
- Free plan limit: restore to 2 before launch (currently 9999 dev)
- taplink-logo.png in static/img/ (for QR logo embed)
- Admin Panel (Page 8)

## Known Issues / Dev Notes
- `qrcode` import: use `colormasks` (plural), not `colormask`
- testuser: Standard plan until 2027-06-16
- Dev login: `/dev-login/` (DEBUG only)
- Dev profile: `http://127.0.0.1:8000/@testuser/`
- QR page: `http://127.0.0.1:8000/dashboard/qr/`

## Evolution of Decisions
- 2026-06-16 Session 1: Project init, Pages 1-4
- 2026-06-16 Session 2: Per-link fonts/colors, username change, plain button style
- 2026-06-17 Session 3: Pages 5-7, gift codes, public profile, QR editor, UX fixes
