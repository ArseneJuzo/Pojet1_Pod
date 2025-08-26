from django.urls import path
from S2CR_App.views.tech_views import *

urlpatterns = [
    path('dashboard/', tech_dashboard, name='tech_dashboard'),
    path('interventions/', my_interventions, name='my_interventions'),
]