from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
import json
import io
import base64
from accounts.models import UserProfile, Link, Appearance
from analytics_app.models import ProfileView, LinkClick
from django_ratelimit.decorators import ratelimit

FREE_LINK_LIMIT = 2
STANDARD_LINK_LIMIT = 10

PLATFORM_ICONS = [
    # Social
    {'id': 'tiktok',     'label': 'TikTok',      'icon': 'music_video',     'category': 'Social'},
    {'id': 'instagram',  'label': 'Instagram',    'icon': 'photo_camera',    'category': 'Social'},
    {'id': 'youtube',    'label': 'YouTube',      'icon': 'smart_display',   'category': 'Social'},
    {'id': 'facebook',   'label': 'Facebook',     'icon': 'thumb_up',        'category': 'Social'},
    {'id': 'twitter',    'label': 'X / Twitter',  'icon': 'alternate_email', 'category': 'Social'},
    {'id': 'linkedin',   'label': 'LinkedIn',     'icon': 'work',            'category': 'Social'},
    {'id': 'discord',    'label': 'Discord',      'icon': 'headset_mic',     'category': 'Social'},
    {'id': 'telegram',   'label': 'Telegram',     'icon': 'send',            'category': 'Social'},
    {'id': 'whatsapp',   'label': 'WhatsApp',     'icon': 'chat',            'category': 'Social'},
    {'id': 'line',       'label': 'LINE',         'icon': 'message',         'category': 'Social'},
    {'id': 'wechat',     'label': 'WeChat',       'icon': 'chat_bubble',     'category': 'Social'},
    {'id': 'threads',    'label': 'Threads',      'icon': 'timeline',        'category': 'Social'},
    # Shopping
    {'id': 'shopee',     'label': 'Shopee',       'icon': 'shopping_bag',    'category': 'Shopping'},
    {'id': 'lazada',     'label': 'Lazada',       'icon': 'local_mall',      'category': 'Shopping'},
    {'id': 'amazon',     'label': 'Amazon',       'icon': 'storefront',      'category': 'Shopping'},
    {'id': 'etsy',       'label': 'Etsy',         'icon': 'handmade',        'category': 'Shopping'},
    # Food & Delivery
    {'id': 'grabfood',   'label': 'GrabFood',     'icon': 'delivery_dining', 'category': 'Food'},
    {'id': 'foodpanda',  'label': 'Foodpanda',    'icon': 'restaurant',      'category': 'Food'},
    {'id': 'lineman',    'label': 'LINE MAN',     'icon': 'moped',           'category': 'Food'},
    # Travel
    {'id': 'grab',       'label': 'Grab',         'icon': 'local_taxi',      'category': 'Travel'},
    {'id': 'airbnb',     'label': 'Airbnb',       'icon': 'house',           'category': 'Travel'},
    {'id': 'agoda',      'label': 'Agoda',        'icon': 'hotel',           'category': 'Travel'},
    # Music
    {'id': 'spotify',    'label': 'Spotify',      'icon': 'library_music',   'category': 'Music'},
    {'id': 'applemusic', 'label': 'Apple Music',  'icon': 'headphones',      'category': 'Music'},
    {'id': 'soundcloud', 'label': 'SoundCloud',   'icon': 'cloud',           'category': 'Music'},
    # Other
    {'id': 'website',    'label': 'Website',      'icon': 'public',          'category': 'Other'},
    {'id': 'email',      'label': 'Email',        'icon': 'mail',            'category': 'Other'},
    {'id': 'phone',      'label': 'Phone',        'icon': 'call',            'category': 'Other'},
    {'id': 'location',   'label': 'Location',     'icon': 'location_on',     'category': 'Other'},
]


@login_required
def home(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.onboarded:
        return redirect('accounts:onboarding')
    appearance, _ = Appearance.objects.get_or_create(user=request.user)
    links = Link.objects.filter(user=request.user)
    limit = STANDARD_LINK_LIMIT if profile.is_standard else FREE_LINK_LIMIT

    icons_by_cat = {}
    for icon in PLATFORM_ICONS:
        cat = icon['category']
        icons_by_cat.setdefault(cat, []).append(icon)

    return render(request, 'dashboard/home.html', {
        'profile': profile,
        'appearance': appearance,
        'links': links,
        'link_count': links.count(),
        'link_limit': limit,
        'at_limit': links.count() >= limit,
        'icons_by_cat': icons_by_cat,
        'platform_icons_json': json.dumps(PLATFORM_ICONS),
    })


@login_required
@require_POST
def link_create(request):
    profile = request.user.profile
    limit = STANDARD_LINK_LIMIT if profile.is_standard else FREE_LINK_LIMIT
    if Link.objects.filter(user=request.user).count() >= limit:
        return JsonResponse({'ok': False, 'error': 'Link limit reached.'}, status=400)
    link = Link.objects.create(
        user=request.user,
        title='New link',
        url='https://',
        order=Link.objects.filter(user=request.user).count()
    )
    return JsonResponse({
        'ok': True,
        'id': link.id,
        'title': link.title,
        'url': link.url,
        'icon': link.icon,
        'color': link.color,
        'text_color': link.text_color,
        'icon_color': link.icon_color,
        'font_family': link.font_family,
        'is_active': link.is_active,
        'order': link.order,
        'display_style': link.display_style,
        'thumbnail_url': link.thumbnail_url,
    })


@login_required
@require_POST
def link_update(request, pk):
    link = get_object_or_404(Link, pk=pk, user=request.user)
    data = json.loads(request.body)
    for field in ('title', 'url', 'icon', 'color', 'text_color', 'icon_color', 'font_family', 'display_style', 'thumbnail_url', 'is_active'):
        if field in data:
            setattr(link, field, data[field])
    link.save()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def link_delete(request, pk):
    link = get_object_or_404(Link, pk=pk, user=request.user)
    link.delete()
    for i, lnk in enumerate(Link.objects.filter(user=request.user)):
        lnk.order = i
        lnk.save(update_fields=['order'])
    return JsonResponse({'ok': True})


@login_required
@require_POST
def link_reorder(request):
    data = json.loads(request.body)
    order_list = data.get('order', [])
    for i, link_id in enumerate(order_list):
        Link.objects.filter(pk=link_id, user=request.user).update(order=i)
    return JsonResponse({'ok': True})


@login_required
@require_POST
def appearance_save(request):
    data = json.loads(request.body)
    appearance, _ = Appearance.objects.get_or_create(user=request.user)
    profile = request.user.profile

    allowed_appearance = [
        'avatar_shape', 'border_color', 'border_width',
        'bg_type', 'bg_color', 'bg_color2', 'bg_gradient_dir', 'bg_video_url',
        'bg_image_pos_x', 'bg_image_pos_y',
        'btn_style', 'btn_color', 'btn_text_color', 'btn_radius', 'btn_hover',
        'font_family', 'font_size', 'text_color',
        'social_icon_style', 'social_icon_size',
    ]
    for field in allowed_appearance:
        if field in data:
            setattr(appearance, field, data[field])
    appearance.save()

    allowed_profile = ['display_name', 'bio', 'location']
    for field in allowed_profile:
        if field in data:
            setattr(profile, field, data[field])
    profile.save()

    return JsonResponse({'ok': True})


@login_required
@require_POST
def username_change(request):
    import re
    from accounts.views import BANNED_USERNAMES
    data = json.loads(request.body)
    new_username = data.get('username', '').strip().lower()
    profile = request.user.profile

    if not new_username:
        return JsonResponse({'ok': False, 'error': 'Username cannot be empty.'}, status=400)
    if not re.match(r'^[a-z0-9_\-]{3,30}$', new_username):
        return JsonResponse({'ok': False, 'error': 'Letters, numbers, _ and - only. 3–30 characters.'}, status=400)
    if new_username in BANNED_USERNAMES:
        return JsonResponse({'ok': False, 'error': 'This username is not available.'}, status=400)
    if new_username == profile.username:
        return JsonResponse({'ok': False, 'error': 'That is already your username.'}, status=400)
    from accounts.models import UserProfile
    if UserProfile.objects.filter(username=new_username).exists():
        return JsonResponse({'ok': False, 'error': 'Username is already taken.'}, status=400)

    profile.username = new_username
    profile.save(update_fields=['username'])
    return JsonResponse({'ok': True, 'username': new_username})


@login_required
@require_POST
def settings_save(request):
    data = json.loads(request.body)
    profile = request.user.profile
    for field in ('display_name', 'bio', 'location', 'birth_year', 'seo_title', 'seo_description', 'is_paused', 'marketing'):
        if field in data:
            setattr(profile, field, data[field])
    profile.save()
    return JsonResponse({'ok': True})


@login_required
@require_POST
def account_delete(request):
    data = json.loads(request.body)
    username = data.get('username', '')
    if username != request.user.profile.username:
        return JsonResponse({'ok': False, 'error': 'Username does not match.'}, status=400)
    request.user.delete()
    return JsonResponse({'ok': True, 'redirect': '/'})


# ─── AVATAR UPLOAD ────────────────────────────────────────────────────────────

@login_required
@require_POST
@ratelimit(key='user', rate='20/h')
def avatar_upload(request):
    if getattr(request, 'limited', False):
        return JsonResponse({'ok': False, 'error': 'Too many uploads. Try again later.'}, status=429)
    from PIL import Image
    from django.core.files.base import ContentFile

    f = request.FILES.get('avatar')
    if not f:
        return JsonResponse({'ok': False, 'error': 'No file provided.'}, status=400)

    is_gif = f.content_type == 'image/gif' or f.name.lower().endswith('.gif')

    if is_gif:
        if f.size > 5 * 1024 * 1024:
            return JsonResponse({'ok': False, 'error': 'GIF max 5 MB olabilir.'}, status=400)
        profile = request.user.profile
        if profile.avatar:
            profile.avatar.delete(save=False)
        profile.avatar.save(f'av_{request.user.id}.gif', f, save=True)
        return JsonResponse({'ok': True, 'url': profile.avatar.url})

    if f.size > 2 * 1024 * 1024:
        return JsonResponse({'ok': False, 'error': 'File too large. Max 2 MB.'}, status=400)

    try:
        img = Image.open(f).convert('RGB')
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Invalid image file.'}, status=400)

    # Center-crop to square then resize to 400×400
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    img = img.resize((400, 400), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=88, optimize=True)
    buf.seek(0)

    profile = request.user.profile
    if profile.avatar:
        profile.avatar.delete(save=False)
    profile.avatar.save(f'av_{request.user.id}.jpg', ContentFile(buf.read()), save=True)
    return JsonResponse({'ok': True, 'url': profile.avatar.url})


# ─── BACKGROUND UPLOAD ─────────────────────────────────────────────────────────

@login_required
@require_POST
@ratelimit(key='user', rate='20/h')
def background_upload(request):
    if getattr(request, 'limited', False):
        return JsonResponse({'ok': False, 'error': 'Too many uploads. Try again later.'}, status=429)
    from PIL import Image
    from django.core.files.base import ContentFile

    f = request.FILES.get('background')
    if not f:
        return JsonResponse({'ok': False, 'error': 'No file provided.'}, status=400)
    if f.size > 8 * 1024 * 1024:
        return JsonResponse({'ok': False, 'error': 'File too large. Max 8 MB.'}, status=400)

    try:
        img = Image.open(f).convert('RGB')
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Invalid image file.'}, status=400)

    # Resize to max 1920×1080 keeping aspect ratio
    img.thumbnail((1920, 1080), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=85, optimize=True)
    buf.seek(0)

    appearance, _ = Appearance.objects.get_or_create(user=request.user)
    if appearance.bg_image:
        appearance.bg_image.delete(save=False)
    appearance.bg_image.save(f'bg_{request.user.id}.jpg', ContentFile(buf.read()), save=True)
    return JsonResponse({'ok': True, 'url': appearance.bg_image.url})


# ─── QR CODE ──────────────────────────────────────────────────────────────────

def _hex_to_rgb(hex_color, fallback=(0, 0, 0)):
    try:
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        return fallback


def _make_qr_image(url, fg='#000000', bg='#ffffff', style='square', padding=4):
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers.pil import (
        SquareModuleDrawer, RoundedModuleDrawer, CircleModuleDrawer,
    )
    from qrcode.image.styles.colormasks import SolidFillColorMask

    drawer = {
        'square':  SquareModuleDrawer(),
        'rounded': RoundedModuleDrawer(),
        'dot':     CircleModuleDrawer(),
    }.get(style, SquareModuleDrawer())

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=max(1, int(padding)),
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=drawer,
        color_mask=SolidFillColorMask(
            front_color=_hex_to_rgb(fg),
            back_color=_hex_to_rgb(bg, (255, 255, 255)),
        ),
    )
    return img.convert('RGBA')


def _embed_logo(qr_img, logo_file, logo_ratio=0.25):
    from PIL import Image
    logo = Image.open(logo_file).convert('RGBA')
    qw, qh = qr_img.size
    size = int(min(qw, qh) * max(0.1, min(0.4, logo_ratio)))
    logo = logo.resize((size, size), Image.LANCZOS)
    # White padding behind logo
    pad = 8
    bg = Image.new('RGBA', (size + pad * 2, size + pad * 2), (255, 255, 255, 255))
    bg.paste(logo, (pad, pad), logo)
    x = (qw - bg.width) // 2
    y = (qh - bg.height) // 2
    qr_img.paste(bg, (x, y), bg)
    return qr_img


def _qr_to_base64(img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


@login_required
def qr_page(request):
    profile = request.user.profile
    url = f'https://{profile.username}.taplink.my/'
    img = _make_qr_image(url)
    initial_qr = _qr_to_base64(img)
    return render(request, 'dashboard/qr.html', {
        'profile': profile,
        'qr_url': url,
        'initial_qr': initial_qr,
    })


@login_required
@require_POST
def qr_preview(request):
    profile = request.user.profile
    if not profile.is_standard:
        return JsonResponse({'error': 'Standard only'}, status=403)

    data = json.loads(request.body)
    url   = f'https://{profile.username}.taplink.my/'
    fg    = data.get('fg', '#000000')
    bg    = data.get('bg', '#ffffff')
    style = data.get('style', 'square')
    pad   = int(data.get('padding', 4))

    img = _make_qr_image(url, fg=fg, bg=bg, style=style, padding=pad)

    if data.get('logo') == 'taplink':
        import os
        from django.conf import settings as dj_settings
        logo_path = os.path.join(dj_settings.BASE_DIR, 'static', 'img', 'taplink-logo.png')
        if os.path.exists(logo_path):
            img = _embed_logo(img, logo_path, float(data.get('logo_size', 0.25)))
    elif data.get('logo') == 'custom' and data.get('logo_data'):
        logo_bytes = base64.b64decode(data['logo_data'].split(',')[-1])
        img = _embed_logo(img, io.BytesIO(logo_bytes), float(data.get('logo_size', 0.25)))

    return JsonResponse({'data_url': _qr_to_base64(img)})


@login_required
def qr_download(request):
    profile = request.user.profile
    fmt    = request.GET.get('format', 'png')
    fg     = request.GET.get('fg', '#000000')
    bg     = request.GET.get('bg', '#ffffff')
    style  = request.GET.get('style', 'square')
    pad    = int(request.GET.get('padding', 4))
    logo   = request.GET.get('logo', 'none')

    url = f'https://{profile.username}.taplink.my/'

    if fmt == 'svg' and not profile.is_standard:
        return HttpResponse('Standard plan required', status=403)
    if style != 'square' and not profile.is_standard:
        style = 'square'
    if fg != '#000000' and not profile.is_standard:
        fg = '#000000'
    if bg != '#ffffff' and not profile.is_standard:
        bg = '#ffffff'

    if fmt == 'svg':
        import qrcode
        import qrcode.image.svg
        qr = qrcode.QRCode(border=pad)
        qr.add_data(url)
        qr.make(fit=True)
        svg_img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        buf = io.BytesIO()
        svg_img.save(buf)
        return HttpResponse(
            buf.getvalue(),
            content_type='image/svg+xml',
            headers={'Content-Disposition': f'attachment; filename="taplink-qr.svg"'},
        )

    img = _make_qr_image(url, fg=fg, bg=bg, style=style, padding=pad)

    if logo == 'taplink' and profile.is_standard:
        import os
        from django.conf import settings as dj_settings
        logo_path = os.path.join(dj_settings.BASE_DIR, 'static', 'img', 'taplink-logo.png')
        if os.path.exists(logo_path):
            img = _embed_logo(img, logo_path, float(request.GET.get('logo_size', 0.25)))

    # 512×512 PNG
    from PIL import Image
    img_rgb = Image.new('RGB', img.size, (int(bg[1:3], 16), int(bg[3:5], 16), int(bg[5:7], 16)))
    img_rgb.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
    img_512 = img_rgb.resize((512, 512), Image.LANCZOS)

    buf = io.BytesIO()
    img_512.save(buf, format='PNG')
    return HttpResponse(
        buf.getvalue(),
        content_type='image/png',
        headers={'Content-Disposition': 'attachment; filename="taplink-qr.png"'},
    )


# ─── ANALYTICS ────────────────────────────────────────────────────────────────

@login_required
def analytics(request):
    profile = request.user.profile
    if not profile.is_standard:
        return redirect('dashboard:home')

    period = request.GET.get('period', '7')
    now = timezone.now()

    if period == '30':
        since = now - timedelta(days=30)
        days = 30
    elif period == 'all':
        since = None
        days = None
    else:
        period = '7'
        since = now - timedelta(days=7)
        days = 7

    views_qs = ProfileView.objects.filter(user=request.user)
    clicks_qs = LinkClick.objects.filter(user=request.user)

    if since:
        views_qs = views_qs.filter(created_at__gte=since)
        clicks_qs = clicks_qs.filter(created_at__gte=since)

    total_views = views_qs.count()
    total_clicks = clicks_qs.count()
    ctr = round((total_clicks / total_views * 100), 1) if total_views else 0

    # Device breakdown for views
    device_counts = defaultdict(int)
    for v in views_qs.values('device'):
        device_counts[v['device']] += 1

    # Daily chart data (only for 7/30 day periods)
    chart_labels = []
    chart_views = []
    chart_clicks = []

    if days:
        daily_views = defaultdict(int)
        daily_clicks = defaultdict(int)

        for v in views_qs.values('created_at'):
            day = v['created_at'].astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d')
            daily_views[day] += 1

        for c in clicks_qs.values('created_at'):
            day = c['created_at'].astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d')
            daily_clicks[day] += 1

        for i in range(days - 1, -1, -1):
            d = (now - timedelta(days=i)).strftime('%Y-%m-%d')
            label = (now - timedelta(days=i)).strftime('%b %d')
            chart_labels.append(label)
            chart_views.append(daily_views.get(d, 0))
            chart_clicks.append(daily_clicks.get(d, 0))

    # Per-link click breakdown
    link_stats = defaultdict(lambda: {'title': '', 'clicks': 0})
    for c in clicks_qs.values('link_id', 'link_title'):
        lid = c['link_id']
        link_stats[lid]['title'] = c['link_title']
        link_stats[lid]['clicks'] += 1

    link_rows = sorted(link_stats.values(), key=lambda x: x['clicks'], reverse=True)

    device_rows = [
        {'label': 'Mobile',  'count': device_counts.get('mobile', 0)},
        {'label': 'Desktop', 'count': device_counts.get('desktop', 0)},
        {'label': 'Tablet',  'count': device_counts.get('tablet', 0)},
    ]

    return render(request, 'dashboard/analytics.html', {
        'profile': profile,
        'period': period,
        'total_views': total_views,
        'total_clicks': total_clicks,
        'ctr': ctr,
        'device_rows': device_rows,
        'mobile_count': device_counts.get('mobile', 0),
        'chart_labels': json.dumps(chart_labels),
        'chart_views': json.dumps(chart_views),
        'chart_clicks': json.dumps(chart_clicks),
        'link_rows': link_rows,
    })
