from django.shortcuts import render, redirect
from accounts.models import UserProfile, Link, Appearance


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

    try:
        appearance = profile.user.appearance
    except Appearance.DoesNotExist:
        appearance, _ = Appearance.objects.get_or_create(user=profile.user)

    links = Link.objects.filter(user=profile.user, is_active=True).order_by('order')

    # Background CSS
    bg = appearance
    if bg.bg_type == 'gradient':
        bg_style = f'background:linear-gradient({bg.bg_gradient_dir},{bg.bg_color},{bg.bg_color2});'
    elif bg.bg_type == 'image' and bg.bg_image:
        bg_style = f'background-image:url({bg.bg_image.url});background-size:cover;background-position:center;background-attachment:fixed;'
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

        entry = {
            'link': link,
            'btn_css': _build_btn_css(link, appearance),
            'border_radius': f'{appearance.btn_radius}px',
            'hover': appearance.btn_hover,
            'platform_color': platform_color,
            'social_icon_color': social_icon_color,
            'is_material': link.icon_type == 'material',
        }

        if link.display_style == 'icon_only':
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
    # TODO: record click event when analytics model is ready
    return redirect(link.url)
