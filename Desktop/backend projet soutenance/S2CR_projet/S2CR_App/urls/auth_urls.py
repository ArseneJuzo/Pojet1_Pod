from django.urls import path
from S2CR_App.views.auth_views import *

urlpatterns = [
    path('login/', connexion_view, name='login'),
    path('register/', inscription_view, name='register'),
    path('logout/', deconnexion_view, name='logout'),
]