import secrets
import string
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from .models import UserProfile, Link, Appearance, GiftCode


def _generate_unique_code():
    """Generate a unique 12-char code in XXXX-XXXX-XXXX format."""
    alphabet = string.ascii_uppercase + string.digits
    # Remove ambiguous chars: 0/O, 1/I/L
    alphabet = alphabet.translate(str.maketrans('', '', '0O1IL'))
    while True:
        raw = ''.join(secrets.choice(alphabet) for _ in range(12))
        code = f'{raw[0:4]}-{raw[4:8]}-{raw[8:12]}'
        if not GiftCode.objects.filter(code=code).exists():
            return code


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'user', 'plan', 'plan_expires', 'onboarded', 'created_at')
    list_filter = ('plan', 'onboarded')
    search_fields = ('username', 'user__email', 'display_name')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'url', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'user__username')


@admin.register(Appearance)
class AppearanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'btn_style', 'bg_type', 'updated_at')


@admin.register(GiftCode)
class GiftCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'plan', 'duration_days', 'is_used', 'used_by', 'used_at', 'created_at')
    list_filter = ('is_used', 'plan')
    search_fields = ('code', 'used_by__username')
    readonly_fields = ('used_by', 'used_at', 'created_at')

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('generate/', self.admin_site.admin_view(self.generate_view), name='giftcode_generate'),
        ]
        return custom + urls

    def generate_view(self, request):
        generated = []

        if request.method == 'POST':
            try:
                count = int(request.POST.get('count', 1))
                duration = int(request.POST.get('duration_days', 30))
                count = max(1, min(count, 10))
                duration = max(1, min(duration, 365))
            except (ValueError, TypeError):
                count, duration = 1, 30

            for _ in range(count):
                code = _generate_unique_code()
                gc = GiftCode.objects.create(code=code, duration_days=duration)
                generated.append(gc)

            messages.success(request, f'{count} gift code{"s" if count > 1 else ""} generated successfully.')

        context = {
            **self.admin_site.each_context(request),
            'title': 'Generate Gift Codes',
            'generated': generated,
            'opts': self.model._meta,
        }
        return render(request, 'admin/accounts/giftcode/generate.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_url'] = 'generate/'
        return super().changelist_view(request, extra_context=extra_context)
