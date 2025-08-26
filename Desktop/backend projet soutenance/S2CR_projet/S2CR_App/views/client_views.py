# S2CR_App/views/client_views.py
from django.shortcuts import render
from django.http import HttpResponse

def client_dashboard(request):
    return HttpResponse("Tableau de bord client")

def client_tickets(request):
    return HttpResponse("Tickets client")

def client_profile(request):
    return HttpResponse("Profil client")