from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here. (Using class based views)

#View for login
class LoginView(View):
    template_name = 'registration/login.html'
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})
        
class RegisterView(View):
    template_name = 'registration/register.html'
    def get(self, request):
        form = StudentRegistrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponse("Form is valid")
        else:
            return render(request, self.template_name, {'form': form})

# @login_required(login_url='main-login')
# def organiser_view(request):
#     if(request.user.role!='organizer'):
#         return redirect("index")
#     event_list = Organized_by.objects.filter(organizer_id=request.user