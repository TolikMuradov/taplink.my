from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('upgrade/redeem/', views.redeem_gift_code, name='redeem_gift_code'),
    path('dev-login/', views.dev_login, name='dev_login'),
]
