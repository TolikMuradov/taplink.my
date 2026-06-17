from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('links/create/', views.link_create, name='link_create'),
    path('links/<int:pk>/update/', views.link_update, name='link_update'),
    path('links/<int:pk>/delete/', views.link_delete, name='link_delete'),
    path('links/reorder/', views.link_reorder, name='link_reorder'),
    path('appearance/save/', views.appearance_save, name='appearance_save'),
    path('settings/save/', views.settings_save, name='settings_save'),
    path('settings/username/', views.username_change, name='username_change'),
    path('account/delete/', views.account_delete, name='account_delete'),
]
