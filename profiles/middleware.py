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
