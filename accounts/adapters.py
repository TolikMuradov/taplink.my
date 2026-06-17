from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect


class TaplinkSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        return '/accounts/onboarding/'

    def get_login_redirect_url(self, request):
        user = request.user
        try:
            profile = user.profile
            if not profile.onboarded:
                return '/accounts/onboarding/'
        except Exception:
            return '/accounts/onboarding/'
        return '/dashboard/'
