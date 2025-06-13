"""
URL configuration for the cdt app.
"""
from django.urls import path
from .views import (
    UserAPIView, UserDetailAPIView,
    PreferenciasAPIView, PreferenciasDetailAPIView,
    NismanAPIView
)

urlpatterns = [
    # User endpoints
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
    
    # Preferences endpoints
    path('preferencias/', PreferenciasAPIView.as_view(), name='preferencias'),
    path('preferencias/<int:user_id>/', PreferenciasDetailAPIView.as_view(), name='preferencias-detail'),
    
    # Nisman endpoint
    path('nisman/', NismanAPIView.as_view(), name='nisman'),
] 