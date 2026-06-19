import hashlib
import re
from urllib.parse import quote
from django.shortcuts import render, redirect
from accounts.models import UserProfile, Link, Appearance
from analytics_app.models import ProfileView, LinkClick


def _parse_youtube_id(url):
    if not url:
        return None
    m = re.search(r'(?:youtu\.be/|youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/))([A-Za-z0-9_-]{11})', url)
    return m.group(1) if m else None


def _get_embed(link):
    """Return (embed_url, embed_height) for media link types, or (None, 0)."""
    url = link.url or ''
    lt = link.link_type

    if lt == 'spotify':
        m = re.search(r'spotify\.com/(track|album|playlist|artist|episode|show)/([A-Za-z0-9]+)', url)
        if m:
            kind, sid = m.group(1), m.group(2)
            height = 152 if kind == 'track' else 352
            return f'https://open.spotify.com/embed/{kind}/{sid}?utm_source=generator', height

    elif lt == 'youtube':
        vid = _parse_youtube_id(url)
        if vid:
            return f'https://www.youtube.com/embed/{vid}', 315
        m = re.search(r'youtube\.com/playlist\?.*?list=([A-Za-z0-9_-]+)', url)
        if m:
            return f'https://www.youtube.com/embed/videoseries?list={m.group(1)}', 315

    elif lt == 'soundcloud':
        if 'soundcloud.com/' in url:
            return f'https://w.soundcloud.com/player/?url={quote(url)}&color=%23ff5500&auto_play=false&hide_related=true&show_comments=false&show_user=true&visual=true', 300

    elif lt == 'apple_music':
        m = re.search(r'music\.apple\.com/(.+)', url)
        if m:
            return f'https://embed.music.apple.com/{m.group(1)}', 450

    elif lt == 'deezer':
        m = re.search(r'deezer\.com/(track|album|playlist|artist)/(\d+)', url)
        if m:
            return f'https://widget.deezer.com/widget/dark/{m.group(1)}/{m.group(2)}', 300

    elif lt == 'tidal':
        type_map = {'track': 'tracks', 'album': 'albums', 'playlist': 'playlists'}
        m = re.search(r'tidal\.com/browse/(track|album|playlist)/(\d+)', url)
        if m:
            return f'https://embed.tidal.com/{type_map.get(m.group(1), "tracks")}/{m.group(2)}', 300

    elif lt == 'bandcamp':
        m = re.search(r'(https?://[^/]+\.bandcamp\.com/(track|album)/[^?#\s]+)', url)
        if m:
            return f'https://bandcamp.com/EmbeddedPlayer/v=2/track={quote(m.group(1))}/size=large/bgcol=1a1a2e/linkcol=a5b4fc/', 120

    elif lt == 'podcast':
        m = re.search(r'spotify\.com/(episode|show)/([A-Za-z0-9]+)', url)
        if m:
            return f'https://open.spotify.com/embed/{m.group(1)}/{m.group(2)}', 232

    elif lt == 'tiktok_video':
        m = re.search(r'tiktok\.com/@[\w.\-]+/video/(\d+)', url)
        if m:
            return f'https://www.tiktok.com/embed/v2/{m.group(1)}', 700

    elif lt == 'vimeo':
        m = re.search(r'vimeo\.com/(?:video/)?(\d+)', url)
        if m:
            return f'https://player.vimeo.com/video/{m.group(1)}?title=0&byline=0&portrait=0', 315

    elif lt == 'audiomack':
        m = re.search(r'audiomack\.com/([^/]+)/(song|album|playlist)/([^/?#\s]+)', url)
        if m:
            return f'https://audiomack.com/embed/{m.group(1)}/{m.group(2)}/{m.group(3)}', 252

    elif lt == 'pdf':
        if url and url not in ('#', 'https://'):
            return f'https://docs.google.com/viewer?url={quote(url)}&embedded=true', 600

    elif lt == 'video':
        if url and url not in ('#', 'https://'):
            return 'video:' + url, 0  # sentinel for <video> tag

    elif lt == 'audio':
        if url and url not in ('#', 'https://'):
            return 'audio:' + url, 0  # sentinel for <audio> tag

    return None, 0


def _get_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '')


def _hash_ip(ip):
    return hashlib.sha256(ip.encode()).hexdigest()[:32]


def _get_device(ua):
    ua = ua.lower()
    if any(x in ua for x in ('mobile', 'android', 'iphone')):
        return 'mobile'
    if any(x in ua for x in ('tablet', 'ipad')):
        return 'tablet'
    return 'desktop'


# Platform brand colors for icon badges
PLATFORM_COLORS = {
    'tiktok': '#000000', 'instagram': '#E1306C', 'youtube': '#FF0000',
    'facebook': '#1877F2', 'twitter': '#1DA1F2', 'x': '#000000',
    'pinterest': '#E60023', 'snapchat': '#FFFC00', 'linkedin': '#0A66C2',
    'reddit': '#FF4500', 'twitch': '#9146FF', 'discord': '#5865F2',
    'telegram': '#2AABEE', 'whatsapp': '#25D366', 'wechat': '#07C160',
    'line': '#00B900', 'viber': '#7360F2', 'bereal': '#000000',
    'threads': '#000000', 'shopee': '#EE4D2D', 'lazada': '#F57224',
    'amazon': '#FF9900', 'ebay': '#E53238', 'etsy': '#F56400',
    'grabfood': '#00B14F', 'foodpanda': '#D70F64', 'grab': '#00B14F',
    'spotify': '#1DB954', 'soundcloud': '#FF5500', 'applemusic': '#FC3C44',
    'airbnb': '#FF5A5F', 'booking': '#003580', 'agoda': '#EB1A23',
}


def _build_btn_css(link, appearance):
    c = link.color or '#8083ff'
    t = link.text_color or '#ffffff'
    s = appearance.btn_style

    if s == 'filled':
        return f'background:{c};color:{t};border:none;'
    elif s == 'outline':
        return f'background:transparent;color:{c};border:2px solid {c};'
    elif s == 'soft':
        return f'background:{c}33;color:{c};border:none;'
    elif s == 'shadow':
        return f'background:{c};color:{t};border:none;box-shadow:0 4px 20px {c}66;'
    elif s == 'glass':
        return f'background:rgba(255,255,255,0.12);color:{t};border:1px solid rgba(255,255,255,0.2);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);'
    elif s == 'gradient':
        return f'background:linear-gradient(135deg,{c},{c}99);color:{t};border:none;'
    elif s == 'plain':
        return f'background:transparent;color:{c};border:none;'
    return f'background:{c};color:{t};border:none;'


def public_profile(request, username):
    try:
        profile = UserProfile.objects.select_related('user').get(username__iexact=username)
    except UserProfile.DoesNotExist:
        return render(request, 'profiles/not_found.html', status=404)

    if profile.is_paused:
        return render(request, 'profiles/paused.html', {'profile': profile})

    # Track profile view (skip owner's own visits)
    if not (request.user.is_authenticated and request.user == profile.user):
        ua = request.META.get('HTTP_USER_AGENT', '')
        ProfileView.objects.create(
            user=profile.user,
            ip_hash=_hash_ip(_get_ip(request)),
            device=_get_device(ua),
        )

    try:
        appearance = profile.user.appearance
    except Appearance.DoesNotExist:
        appearance, _ = Appearance.objects.get_or_create(user=profile.user)

    links = Link.objects.filter(user=profile.user, is_active=True).order_by('order')

    # Background CSS
    bg = appearance
    youtube_embed_url = None
    if bg.bg_type == 'gradient':
        bg_style = f'background:linear-gradient({bg.bg_gradient_dir},{bg.bg_color},{bg.bg_color2});'
    elif bg.bg_type == 'image' and bg.bg_image:
        px = getattr(bg, 'bg_image_pos_x', 50)
        py = getattr(bg, 'bg_image_pos_y', 50)
        bg_style = f'background-image:url({bg.bg_image.url});background-size:cover;background-position:{px}% {py}%;background-attachment:fixed;'
    elif bg.bg_type == 'video' and bg.bg_video_url:
        vid_id = _parse_youtube_id(bg.bg_video_url)
        if vid_id:
            youtube_embed_url = f'https://www.youtube.com/embed/{vid_id}?autoplay=1&mute=1&loop=1&playlist={vid_id}&controls=0&playsinline=1'
        bg_style = f'background-color:{bg.bg_color};'
    else:
        bg_style = f'background-color:{bg.bg_color};'

    # Avatar border style
    border_style = ''
    if bg.border_width > 0:
        border_style = f'border:{bg.border_width}px solid {bg.border_color};'

    # Avatar shape
    shape_css = {
        'circle': 'border-radius:50%;',
        'square': 'border-radius:12px;',
    }.get(bg.avatar_shape, 'border-radius:50%;')

    # Icon size for social row
    icon_size = {'small': '18px', 'medium': '22px', 'large': '28px'}.get(bg.social_icon_size, '22px')
    icon_badge_size = {'small': '36px', 'medium': '44px', 'large': '52px'}.get(bg.social_icon_size, '44px')

    # Process links
    social_links = []   # icon_only → compact row
    main_links = []     # icon_text → full buttons

    for link in links:
        platform_color = PLATFORM_COLORS.get(link.icon_type, link.color or '#8083ff')
        icon_color = link.icon_color or '#ffffff'

        # Social icon row color based on style setting
        if bg.social_icon_style == 'white':
            social_icon_color = '#ffffff'
        elif bg.social_icon_style == 'black':
            social_icon_color = '#000000'
        else:
            social_icon_color = icon_color

        embed_url, embed_height = _get_embed(link)
        entry = {
            'link': link,
            'btn_css': _build_btn_css(link, appearance),
            'border_radius': f'{appearance.btn_radius}px',
            'hover': appearance.btn_hover,
            'platform_color': platform_color,
            'social_icon_color': social_icon_color,
            'is_iconify': ':' in link.icon,
            'is_material': ':' not in link.icon and link.icon_type == 'material',
            'embed_url': embed_url,
            'embed_height': embed_height,
        }

        if link.link_type in ('header', 'divider'):
            main_links.append(entry)
        elif link.display_style == 'icon_only':
            social_links.append(entry)
        else:
            main_links.append(entry)

    # Collect unique fonts for Google Fonts
    fonts_used = set()
    if appearance.font_family and appearance.font_family not in ('Inter', ''):
        fonts_used.add(appearance.font_family)
    for link in links:
        if link.font_family:
            fonts_used.add(link.font_family)

    gf_query = '&family='.join(f.replace(' ', '+') + ':wght@400;500;600;700' for f in fonts_used)
    google_fonts_url = f'https://fonts.googleapis.com/css2?family={gf_query}&display=swap' if gf_query else ''

    context = {
        'profile': profile,
        'appearance': appearance,
        'social_links': social_links,
        'main_links': main_links,
        'bg_style': bg_style,
        'youtube_embed_url': youtube_embed_url,
        'border_style': border_style,
        'shape_css': shape_css,
        'icon_size': icon_size,
        'icon_badge_size': icon_badge_size,
        'google_fonts_url': google_fonts_url,
        'text_color': appearance.text_color or '#e4e1ed',
        'global_font': appearance.font_family or 'Inter',
    }
    return render(request, 'profiles/public_profile.html', context)


def link_redirect(request, username, link_id):
    """Redirect for link clicks — analytics hook point for future tracking."""
    try:
        profile = UserProfile.objects.get(username__iexact=username)
        link = Link.objects.get(id=link_id, user=profile.user, is_active=True)
    except (UserProfile.DoesNotExist, Link.DoesNotExist):
        return redirect('/')
    ua = request.META.get('HTTP_USER_AGENT', '')
    LinkClick.objects.create(
        user=profile.user,
        link_id=link.id,
        link_title=link.title,
        ip_hash=_hash_ip(_get_ip(request)),
        device=_get_device(ua),
    )
    return redirect(link.url)
