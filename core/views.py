from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings


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
