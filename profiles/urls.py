from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('@<str:username>/', views.public_profile, name='public_profile'),
    path('@<str:username>/r/<int:link_id>/', views.link_redirect, name='link_redirect'),
]
