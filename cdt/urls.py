"""
URL configuration for the cdt app.
"""
from django.urls import path
from .views import UserAPIView, PreferenciasAPIView, NismanAPIView

urlpatterns = [
    # User endpoints
    path('users/', UserAPIView.as_view(), name='user-list'),
    
    # Preferences endpoints
    path('preferencias/', PreferenciasAPIView.as_view(), name='preferencias'),
    # Nisman endpoint
    path('nisman/', NismanAPIView.as_view(), name='nisman'),
] 