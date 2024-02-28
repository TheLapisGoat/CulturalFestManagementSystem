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
            #Create the user and student
            user = User_Entity.objects.create_user(
                username = form.cleaned_data['username'], 
                password = form.cleaned_data['password'],
                first_name = form.cleaned_data['first_name'],
                middle_name = form.cleaned_data['middle_name'],
                last_name = form.cleaned_data['last_name'], 
                email = form.cleaned_data['email'], 
                address_line_1 = form.cleaned_data['address_line_1'],
                address_line_2 = form.cleaned_data['address_line_2'],
                state = form.cleaned_data['state'],
                country = form.cleaned_data['country'],
                pin_code = form.cleaned_data['pin_code'],
                telephoneNumber = form.cleaned_data['telephoneNumber'],
                photograph = form.cleaned_data['photograph'],
                role = 'student',
                gender = form.cleaned_data['gender'],
                date_of_birth = form.cleaned_data['date_of_birth'],
            )

            student = Student.objects.create(
                user = user,
                roll_number = form.cleaned_data['roll_number'],
                department = form.cleaned_data['department']
            )
            return render(request, self.template_name, {'form': form})

        else:
            return render(request, self.template_name, {'form': form})


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

