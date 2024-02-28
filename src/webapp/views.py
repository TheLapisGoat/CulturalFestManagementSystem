from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the webapp index.")


@login_required(login_url='main-login')
def organiser_view(request):
    if(request.user.role!='organizer'):
        return redirect("index")
    event_list = Organized_by.objects.filter(organizer_id=request.user