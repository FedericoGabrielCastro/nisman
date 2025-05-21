from django.urls import path
from .views import (
    UserAPIView,
    UserDetailAPIView,
    PreferenciasAPIView,
    PreferenciasDetailAPIView
)

app_name = 'tenants'

urlpatterns = [
    # User endpoints
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
    
    # Preferences endpoints
    path('preferencias/', PreferenciasAPIView.as_view(), name='preferencias-list'),
    path('preferencias/<int:user_id>/', PreferenciasDetailAPIView.as_view(), name='preferencias-detail'),
] 