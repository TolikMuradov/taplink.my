from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    PLAN_FREE     = 'free'
    PLAN_STANDARD = 'standard'
    PLAN_CHOICES  = [(PLAN_FREE, 'Free'), (PLAN_STANDARD, 'Standard')]

    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username     = models.CharField(max_length=30, unique=True, blank=True)
    display_name = models.CharField(max_length=60, blank=True)
    bio          = models.CharField(max_length=160, blank=True)
    location     = models.CharField(max_length=60, blank=True)
    birth_year   = models.PositiveSmallIntegerField(null=True, blank=True)
    avatar       = models.ImageField(upload_to='avatars/', null=True, blank=True)
    plan         = models.CharField(max_length=10, choices=PLAN_CHOICES, default=PLAN_FREE)
    plan_expires = models.DateTimeField(null=True, blank=True)
    is_paused    = models.BooleanField(default=False)
    onboarded    = models.BooleanField(default=False)
    marketing    = models.BooleanField(default=False)
    # SEO
    seo_title       = models.CharField(max_length=60, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username or str(self.user)

    @property
    def is_standard(self):
        from django.utils import timezone
        if self.plan == self.PLAN_STANDARD:
            if self.plan_expires is None or self.plan_expires > timezone.now():
                return True
        return False


class Link(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='links')
    title         = models.CharField(max_length=80)
    url           = models.URLField(max_length=500)
    icon          = models.CharField(max_length=40, default='link')        # Material symbol name
    icon_type     = models.CharField(max_length=20, default='material')    # 'material' or platform name
    color         = models.CharField(max_length=7, default='#8083ff')      # button bg / accent color
    text_color    = models.CharField(max_length=7, default='#ffffff')      # label text color
    icon_color    = models.CharField(max_length=7, default='#ffffff')      # icon color
    font_family   = models.CharField(max_length=60, blank=True, default='') # per-link font (empty = global)
    display_style = models.CharField(max_length=20, default='icon_text')   # 'icon_text' or 'icon_only'
    thumbnail_url = models.URLField(max_length=500, blank=True)
    is_active     = models.BooleanField(default=True)
    order         = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.user} — {self.title}'


class Appearance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='appearance')
    # Profile
    avatar_shape  = models.CharField(max_length=10, default='circle')   # circle, square, hexagon
    border_color  = models.CharField(max_length=7, default='#8083ff')
    border_width  = models.PositiveSmallIntegerField(default=2)
    # Background
    bg_type         = models.CharField(max_length=10, default='color')      # color, gradient, image, video
    bg_color        = models.CharField(max_length=7, default='#13131b')
    bg_color2       = models.CharField(max_length=7, default='#1f1f27')
    bg_gradient_dir = models.CharField(max_length=10, default='to bottom')
    bg_image        = models.ImageField(upload_to='backgrounds/', null=True, blank=True)
    bg_video_url    = models.URLField(max_length=500, blank=True)
    # Buttons
    btn_style      = models.CharField(max_length=10, default='filled')     # filled, outline, soft, shadow, glass, gradient
    btn_color      = models.CharField(max_length=7, default='#8083ff')
    btn_text_color = models.CharField(max_length=7, default='#0d0096')
    btn_radius     = models.PositiveSmallIntegerField(default=12)
    btn_hover      = models.BooleanField(default=True)
    # Typography
    font_family = models.CharField(max_length=60, default='Inter')
    font_size   = models.CharField(max_length=10, default='medium')         # small, medium, large
    text_color  = models.CharField(max_length=7, default='#e4e1ed')
    # Social icons
    social_icon_style = models.CharField(max_length=10, default='colorful')  # colorful, white, black
    social_icon_size  = models.CharField(max_length=10, default='medium')    # small, medium, large

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Appearance({self.user})'


class GiftCode(models.Model):
    code         = models.CharField(max_length=32, unique=True)
    plan         = models.CharField(max_length=10, default='standard')
    duration_days = models.PositiveIntegerField(default=30)
    is_used      = models.BooleanField(default=False)
    used_by      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='gift_codes')
    used_at      = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = f'used by {self.used_by}' if self.is_used else 'unused'
        return f'{self.code} ({status})'


@receiver(post_save, sender=User)
def create_appearance(sender, instance, created, **kwargs):
    if created:
        Appearance.objects.get_or_create(user=instance)
