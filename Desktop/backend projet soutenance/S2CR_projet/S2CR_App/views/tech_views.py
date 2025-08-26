from django.shortcuts import render
from django.http import HttpResponse

def tech_dashboard(request):
    return HttpResponse("Tableau de bord tech")

def my_interventions(request):
    return HttpResponse("Tickets client")

