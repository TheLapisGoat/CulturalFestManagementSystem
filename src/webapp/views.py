import threading
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
import asyncio
from .models import *
from .forms import StudentRegistrationForm, OTPVerificationForm
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
            print(user,"User")
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
                is_active = False,
            )

            student = Student.objects.create(
                user = user,
                roll_number = form.cleaned_data['roll_number'],
                department = form.cleaned_data['department']
            )

            #Sending otp to created user's email. If otp is not verified in 5 minutes, delete the user
            otp = default_token_generator.make_token(user)
            subject = 'Festival Management System: Verify your email'
            message = 'Your otp is ' + otp
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, email_from, recipient_list)

            #Storing the necessary data in session
            request.session['otp'] = otp
            request.session['username'] = user.username

            #Schedule a task to delete the user if otp is not verified in 5 minutes
            threading.Timer(30.0, schedule_deletion, [request]).start()

            #Redirect to otp verification page
            return redirect('otp-verification')

        else:
            return render(request, self.template_name, {'form': form})
        
def schedule_deletion(request):
    #Check if the user has verified the otp (is_active = True)
    user = User_Entity.objects.get(username = request.session['username'])
    if user.is_active == False:
        user.delete()

class OTPVerificationView(View):
    template_name = 'registration/otp_verification.html'

    def get(self, request):
        #First check if a user corresponding to the username exists
        if 'username' in request.session:
            username = request.session['username']
            user = User_Entity.objects.filter(username = username)
            if user.exists():
                user = user[0]
                if user.is_active:
                    return redirect('index')
            else:
                return redirect('index')
        else:
            return redirect('index')
        
        form = OTPVerificationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if 'otp' in request.session and otp == request.session['otp']:
                username = request.session.get('username')
                #Check if the user exists, if it does not exist, then the user has been deleted
                user = User_Entity.objects.filter(username = username)
                if user.exists():
                    user = user[0]
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Account created successfully')
                else:
                    form.add_error('otp', 'OTP expired. Please register again.')
            else:
                form.add_error('otp', 'Invalid OTP')
        return render(request, self.template_name, {'form': form})


#@login_required(login_url='main-login')
def organizer_view(request):
    if(request.user.is_anonymous):
        return HttpResponse("You're not logged in")
    if(request.user.role!='organizer'):
        return redirect("index")
    organiser = Organizer.objects.filter(user=request.user).first()
    event_list = Organized_by.objects.filter(organizer_id=organiser)
    event_id_list = event_list.values_list('event_id',flat=True)
    events = list(Event.objects.all())
    res = []
    #for i in range(len(events)):
        #print(events[i])
    for event in events:
        if event.event_id in event_id_list:
            res.append(event)
    return render(request, 'organiser/organiser_view.html', {'events': res})
def organiser_event_view(request, event_id):
    if(request.user.is_anonymous):
        return HttpResponse("You're not logged in")
    if(request.user.role!='organizer'):
        return redirect("index")
    event = get_object_or_404(Event, event_id=event_id)
    return render(request, 'organiser/organiser_event_view.html', {'event': event})


def index(request):
    return HttpResponse("Hello, world. You're at the webapp index.")

        

        
class HomeView(View):
    template_name = 'index.html'
    def get(self, request):
        #Send a mail to a 'sourodeepdatta@gmail.com'
        subject = 'Welcome to the Festival Management System'
        message = 'We are glad to have you here. We hope you have a great time'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['sourodeepdatta@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        return HttpResponse('Mail Sent')