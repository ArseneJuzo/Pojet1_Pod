from django.shortcuts import render
from django.http import HttpResponse

def manage_users(request):
    return HttpResponse("manage_users")

def admin_dashboard(request):
    return HttpResponse("admin_dashboard")

