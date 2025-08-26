# gestion_pannes/urls/__init__.py
from django.urls import path, include

urlpatterns = [
    path('auth/', include('S2CR_App.urls.auth_urls')),
    path('client/', include('S2CR_App.urls.client_urls')),
    path('admin/', include('S2CR_App.urls.admin_urls')),
    path('tech/', include('S2CR_App.urls.tech_urls')),
]