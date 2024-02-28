from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the webapp index.")


#@login_required(login_url='main-login')
def organiser_view(request):
    if(request.user.is_anonymous):
        return HttpResponse("You're not logged in")
    if(request.user.role!='organizer'):
        return redirect("index")
    event_list = Organized_by.objects.filter(organizer_id=request.user)
    event_id_list = event_list.values_list('event_id',flat=True)
    events = Event.objects.all()
    res = []
    for event in events:
        if event.event_id in event_id_list:
            res.append(event)
    return render(request, 'organiser_view.html', {'events': res})
