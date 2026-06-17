import json
import re

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import UserProfile

BANNED_USERNAMES = {
    'admin', 'www', 'api', 'static', 'media', 'mail', 'ftp', 'blog', 'app',
    'dashboard', 'login', 'register', 'support', 'help', 'about', 'contact',
    'terms', 'privacy', 'taplink', 'billing', 'upgrade', 'redeem', 'qr',
    'root', 'test', 'dev', 'null', 'undefined',
}


def _username_is_valid(username):
    return bool(re.match(r'^[a-z0-9_]{3,30}$', username))


@login_required
def onboarding(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if profile.onboarded:
        return redirect('dashboard:home')

    if request.method == 'POST':
        step = request.POST.get('step')

        if step == '1':
            request.session['onboarding_source'] = request.POST.get('source', '')
            request.session['onboarding_use_case'] = request.POST.get('use_case', '')
            request.session['onboarding_birth_year'] = request.POST.get('birth_year', '')
            return JsonResponse({'ok': True})

        elif step == '2':
            username = request.POST.get('username', '').lower().strip()
            terms = request.POST.get('terms') == 'true'
            marketing = request.POST.get('marketing') == 'true'

            if not _username_is_valid(username):
                return JsonResponse({'ok': False, 'error': 'Invalid username format.'})
            if username in BANNED_USERNAMES:
                return JsonResponse({'ok': False, 'error': 'This username is not allowed.'})
            if UserProfile.objects.filter(username=username).exclude(user=request.user).exists():
                return JsonResponse({'ok': False, 'error': 'Username is already taken.'})
            if not terms:
                return JsonResponse({'ok': False, 'error': 'You must accept the Terms of Service.'})

            profile.username = username
            profile.marketing = marketing
            profile.onboarded = True
            # Pull step-1 data from session
            birth_year = request.session.get('onboarding_birth_year', '')
            if birth_year.isdigit():
                profile.birth_year = int(birth_year)
            profile.save()

            # Clean up session
            for k in ('onboarding_source', 'onboarding_use_case', 'onboarding_birth_year'):
                request.session.pop(k, None)

            return JsonResponse({'ok': True, 'redirect': '/dashboard/'})

    return render(request, 'accounts/onboarding.html')


@login_required
@require_GET
def check_username(request):
    username = request.GET.get('username', '').lower().strip()
    if not _username_is_valid(username):
        return JsonResponse({'available': False, 'reason': 'invalid'})
    if username in BANNED_USERNAMES:
        return JsonResponse({'available': False, 'reason': 'banned'})
    taken = UserProfile.objects.filter(username=username).exclude(user=request.user).exists()
    return JsonResponse({'available': not taken})
