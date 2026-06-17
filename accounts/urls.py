from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('onboarding/', views.onboarding, name='onboarding'),
    path('check-username/', views.check_username, name='check_username'),
]
