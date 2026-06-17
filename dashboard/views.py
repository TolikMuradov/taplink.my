from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
import json
from accounts.models import UserProfile, Link, Appearance

FREE_LINK_LIMIT = 9999  # temporarily unlimited for dev
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
        'bg_type', 'bg_color', 'bg_color2', 'bg_gradient_dir',
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
