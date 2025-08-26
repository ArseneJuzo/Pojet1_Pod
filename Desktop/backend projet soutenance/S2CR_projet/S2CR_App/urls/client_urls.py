from django.urls import path
from S2CR_App.views.client_views import *

urlpatterns = [
    path('dashboard/', client_dashboard, name='client_dashboard'),
    path('tickets/', client_tickets, name='client_tickets'),
    # Ajoutez d'autres URLs clients ici
]