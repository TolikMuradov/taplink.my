from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('dev-login/', views.dev_login, name='dev_login'),
]
