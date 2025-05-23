from django.urls import path
from .views import (
    TenantsAPIView,
    NismanAPIView
)

app_name = 'tenants'

urlpatterns = [
    # Tenants endpoint
    path('tenants/', TenantsAPIView.as_view(), name='user-list'),
    
    # Nisman endpoint
    path('tenants/nisman/', NismanAPIView.as_view(), name='nisman'),
] 