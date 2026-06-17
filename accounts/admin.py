from django.contrib import admin
from .models import UserProfile, Link, Appearance, GiftCode


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
