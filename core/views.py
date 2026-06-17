import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django_ratelimit.decorators import ratelimit


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'core/landing.html')


def privacy(request):
    return render(request, 'core/privacy.html')


def terms(request):
    return render(request, 'core/terms.html')


def dev_login(request):
    """DEV ONLY — bypasses Google OAuth. Remove before production."""
    if not settings.DEBUG:
        from django.http import Http404
        raise Http404
    user = authenticate(request, username='testuser', password='test1234')
    if user:
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('dashboard:home')


@login_required
def upgrade(request):
    profile = request.user.profile
    comparison_rows = [
        {'feature': 'Links', 'free': '2', 'standard': '10'},
        {'feature': 'Themes', 'free': '1', 'standard': 'All'},
        {'feature': 'Background video', 'free': '✗', 'standard': '✓'},
        {'feature': 'Custom fonts', 'free': '6 basic', 'standard': '16 fonts'},
        {'feature': 'Analytics', 'free': '✗', 'standard': '✓'},
        {'feature': 'Custom QR code', 'free': '✗', 'standard': '✓'},
        {'feature': 'Animated redirect', 'free': '✗', 'standard': '✓'},
        {'feature': 'Watermark', 'free': '✓', 'standard': '✗'},
    ]
    return render(request, 'core/upgrade.html', {'profile': profile, 'comparison_rows': comparison_rows})


@login_required
@ratelimit(key='user', rate='5/h', method='POST')
def redeem_gift_code(request):
    if getattr(request, 'limited', False):
        return JsonResponse({'error': 'Too many attempts. Please wait before trying again.'}, status=429)
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    from accounts.models import GiftCode
    data = json.loads(request.body)
    code_str = data.get('code', '').strip().upper()

    if not code_str:
        return JsonResponse({'error': 'Please enter a gift code.'}, status=400)

    try:
        gift = GiftCode.objects.get(code=code_str)
    except GiftCode.DoesNotExist:
        return JsonResponse({'error': 'Invalid or already used code.'}, status=400)

    if gift.is_used:
        return JsonResponse({'error': 'Invalid or already used code.'}, status=400)

    profile = request.user.profile
    now = timezone.now()

    # If already Standard and not expired, extend from current expiry
    if profile.plan == 'standard' and profile.plan_expires and profile.plan_expires > now:
        new_expiry = profile.plan_expires + timedelta(days=gift.duration_days)
    else:
        new_expiry = now + timedelta(days=gift.duration_days)

    profile.plan = gift.plan
    profile.plan_expires = new_expiry
    profile.save()

    gift.is_used = True
    gift.used_by = request.user
    gift.used_at = now
    gift.save()

    return JsonResponse({
        'success': True,
        'message': f'🎉 {gift.duration_days} days of Standard activated!',
        'expires': new_expiry.strftime('%B %d, %Y'),
    })
