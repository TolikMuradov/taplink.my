import time
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse

MAIN_DOMAIN = 'taplink.my'
RESERVED = {
    'www', 'api', 'static', 'media', 'mail', 'ftp', 'blog', 'app',
    'dashboard', 'login', 'register', 'support', 'help', 'about',
    'contact', 'terms', 'privacy', 'taplink', 'billing', 'upgrade',
    'redeem', 'qr', 'admin',
}


class SubdomainMiddleware:
    """
    Routes username.taplink.my → public_profile view.
    In dev, use /@username/ path instead.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()

        if host.endswith('.' + MAIN_DOMAIN):
            subdomain = host[: -(len(MAIN_DOMAIN) + 1)]
            if subdomain and subdomain not in RESERVED:
                from profiles.views import public_profile
                return public_profile(request, username=subdomain)

        return self.get_response(request)


class LoginRateLimitMiddleware:
    """
    Limits OAuth login initiations to 20 per minute per IP.
    Targets /accounts/google/login/ and /accounts/login/.
    """
    LIMIT = 20
    WINDOW = 60  # seconds

    LOGIN_PREFIXES = ('/accounts/google/login', '/accounts/login')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET' and request.path.startswith(self.LOGIN_PREFIXES):
            ip = self._get_ip(request)
            key = f'login_rl:{ip}'
            count = cache.get(key, 0)
            if count >= self.LIMIT:
                return HttpResponse(
                    'Too many login attempts. Please wait a moment.',
                    status=429,
                    content_type='text/plain',
                )
            cache.set(key, count + 1, timeout=self.WINDOW)
        return self.get_response(request)

    @staticmethod
    def _get_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '')
