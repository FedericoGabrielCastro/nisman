"""
Main URL configuration for the project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Include URLs from cdt app
    path('api/', include('cdt.urls')),
    
    # Include URLs from tenants app
    path('api/tenants/', include('tenants.urls')),
] 