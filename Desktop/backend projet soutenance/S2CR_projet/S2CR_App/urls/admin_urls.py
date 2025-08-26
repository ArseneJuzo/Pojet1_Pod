from django.urls import path
from S2CR_App.views.admin_views import *

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('users/', manage_users, name='manage_users'),
    
]