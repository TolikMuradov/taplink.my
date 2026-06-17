# Project Brief — taplink.my

## Project Name
**taplink.my** — Link-in-bio platform targeting Thailand market

## Core Goal
Build a full-stack link-in-bio web application where users can create a personalized landing page (`username.taplink.my`) that consolidates their social media, e-commerce, and other links under one shareable URL.

## Target Market
- **Primary:** Thailand
- **Built-in integrations:** TikTok, Instagram, YouTube, Shopee, Lazada, Grab, LINE, WeChat, Spotify, Apple Music and more Thai-relevant platforms

## Business Model
| Plan | Price | Key Limits |
|------|-------|------------|
| Free | 0 THB | 2 links, 1 theme, basic QR, watermark, no analytics, direct redirect |
| Standard | 99 THB/month | 10 links, all themes, custom QR, analytics, no watermark, animated redirects, gift codes |

## Core Requirements
1. Google OAuth only (no passwords, no email auth)
2. Subdomain routing: `username.taplink.my` via Caddy wildcard SSL
3. Dark mode by default across the platform
4. Mobile-first design (public profile max 640px centered)
5. Real-time dashboard with live profile preview
6. Analytics for Standard plan users

## Key Pages
1. **Landing page** (`taplink.my/`) — public marketing page
2. **Login** (`/login`) — Google OAuth only
3. **Onboarding** — 2-step modal (profiling + username selection)
4. **Dashboard** (`/dashboard`) — 3-panel editor (sidebar + editor + preview)
5. **Public Profile** (`username.taplink.my`) — mobile-first link page
6. **Upgrade** (`/upgrade`) — plan comparison + gift code redemption
7. **QR Code** (`/dashboard/qr`) — QR generator
8. **Admin Panel** (`/admin-panel`) — superuser only

## Specification Document
Full UI/UX spec is in `plan.txt` (Turkish, 608 lines) — page-by-page breakdown, intended for sequential AI-assisted implementation.

## Banned Usernames
admin, www, api, static, media, mail, ftp, blog, app, dashboard, login, register, support, help, about, contact, terms, privacy, taplink, billing, upgrade, redeem, qr
