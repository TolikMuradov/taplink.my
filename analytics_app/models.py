from django.db import models
from django.contrib.auth.models import User


class ProfileView(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_views')
    ip_hash    = models.CharField(max_length=32)
    device     = models.CharField(max_length=10, blank=True)   # mobile / tablet / desktop
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user', 'created_at'])]


class LinkClick(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link_clicks')
    link_id    = models.IntegerField()
    link_title = models.CharField(max_length=80)
    ip_hash    = models.CharField(max_length=32)
    device     = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['link_id']),
        ]
