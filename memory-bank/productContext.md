# Product Context — taplink.my

## Why This Project Exists
Thai users (influencers, small business owners, content creators) need a single shareable link that consolidates all their social media, e-commerce, and contact points. Existing solutions (Linktree, Beacons) are not optimized for Thailand's platform ecosystem (Shopee, Lazada, Grab, LINE).

## Problems It Solves
1. **Link fragmentation** — Users can't put multiple links in Instagram/TikTok bios
2. **Thailand-specific platforms** — Pre-built icons for Thai e-commerce and apps
3. **Affordability** — 99 THB/month vs. USD-priced competitors
4. **Simplicity** — Google login only, no password management

## How It Should Work

### User Journey
1. User visits `taplink.my` → sees landing page with live demo mockup
2. Clicks "Create your page" → Google OAuth login
3. Completes 2-step onboarding (profiling + username)
4. Lands on dashboard → adds links, customizes appearance
5. Shares `username.taplink.my` in their bio
6. Visitors click the link → see their curated page, click through to destinations

### Dashboard UX (3-panel layout)
- **Left sidebar** (collapsible): Navigation between tabs + plan badge
- **Center editor**: Tabs — Links | Appearance | Analytics | Settings
- **Right preview** (collapsible): Phone mockup, real-time preview, share button

### Key UX Principles
- **Real-time preview** — all changes show instantly in right panel (no save button needed for most things)
- **Dark mode everywhere** — system default
- **Toast notifications** — green/red/yellow, bottom-right, auto-dismiss 3s
- **Empty states** — illustrated guidance when no content
- **Loading states** — button spinners + skeleton loaders

## User Experience Goals
- Onboarding under 2 minutes
- Dashboard feels intuitive without a tutorial
- Public profile loads fast, looks professional on mobile
- Analytics clear enough for non-technical users
- Upgrade flow feels natural, not pushy

## Competitor Context
Similar to: Linktree, Beacons, Koji, bio.link
Differentiation: Thailand focus, Thai payment (THB), Thai platform icons, local market pricing
