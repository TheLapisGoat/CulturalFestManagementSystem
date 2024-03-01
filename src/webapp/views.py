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
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
import asyncio
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import StudentRegistrationForm, OTPVerificationForm, External_ParticipantRegistrationForm, OrganizerRegistrationForm
from django.utils.decorators import method_decorator
# Create your views here. (Using class based views)

#Redirects to every home page
@method_decorator(login_required(login_url='login'), name='dispatch')
class MainViewRedirect(View):

    def get(self, request):
        if request.user.role == 'student':
            return redirect('student-home')
        elif request.user.role == 'external_participant':
            return redirect('external-participant-home')
        elif request.user.role == 'organizer':
            return redirect('organizer-home')
        elif request.user.role == 'admin':
            return redirect('admin-home')
        else:
            return redirect('login')

#View for login
class LoginView(View):
    template_name = 'registration/login.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index-redirector')
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user,"User")
            login(request, user)
            return redirect('index-redirector')
        else:
            return render(request, self.template_name, {'form': form})
        
class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        form = StudentRegistrationForm()
        request.session['register_current_role'] = 'student'
        return render(request, self.template_name, {'form': form, 'default_role': 'student'})
    
    def post(self, request):

        #Check whether the role was changed or the form was submitted
        action = request.POST.get('action')
        
        #If the role was changed, then return the form with the new role
        if action == 'role_change':
            print('Role changed')
            role = request.POST.get('role')
            request.session['register_current_role'] = role
            if role == 'student':
                form = StudentRegistrationForm()
            elif role == 'external_participant':
                form = External_ParticipantRegistrationForm()
            elif role == 'organizer':
                form = OrganizerRegistrationForm()
            return render(request, self.template_name, {'form': form, 'default_role': role})
        
        #If the form was submitted, then process the form
        form = None
        role = request.session['register_current_role']
        if role == 'student':
            form = StudentRegistrationForm(request.POST, request.FILES)
        elif role == 'external_participant':
            form = External_ParticipantRegistrationForm(request.POST, request.FILES)
        elif role == 'organizer':
            form = OrganizerRegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            #Create the user
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
                role = role, 
                gender = form.cleaned_data['gender'],
                date_of_birth = form.cleaned_data['date_of_birth'],
                is_active = False,
            )
        
            #Creating the models corresponding to the role
            if role == 'student':
                student = Student.objects.create(
                    user = user,
                    roll_number = form.cleaned_data['roll_number'],
                    department = form.cleaned_data['department']
                )
            elif role == 'external_participant':
                participant = External_Participant.objects.create(
                    user = user,
                    organization = form.cleaned_data['organization']
                )
            elif role == 'organizer':
                organizer = Organizer.objects.create(
                    user = user
                )

                #Delete the organizer key
                organizer_key = Organizer_Key.objects.get(key = form.cleaned_data['organizer_key'])
                organizer_key.delete()

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

            extra_args = {}
            extra_args['role'] = role
            if role == 'organizer':
                extra_args['organizer_key'] = form.cleaned_data['organizer_key']

            #Schedule a task to delete the user if otp is not verified in 5 minutes
            threading.Timer(300.0, schedule_deletion, [request, extra_args]).start()

            #Redirect to otp verification page
            return redirect('otp-verification')
        
        else:
            return render(request, self.template_name, {'form': form, 'default_role': request.session['register_current_role']})
        
def schedule_deletion(request, extra_args):
    #Check if the user has verified the otp (is_active = True)
    user = User_Entity.objects.get(username = request.session['username'])
    if user.is_active == False:
        user.delete()
        
        #If the user is an organizer, then create the organizer key again
        if extra_args['role'] == 'organizer':
            organizer_key = Organizer_Key.objects.create(key = extra_args['organizer_key'])
            organizer_key.save()

    #todo: seems like this fn is incomplete

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
                    return redirect('index-redirector')
            else:
                return redirect('index-redirector')
        else:
            return redirect('index-redirector')
        
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
                    if user.is_active == False:
                        user.is_active = True
                        user.save()
                        messages.success(request, 'Account created successfully')
                    else:
                        messages.error(request, 'Account already verified')
                else:
                    form.add_error('otp', 'OTP expired. Please register again.')
            else:
                form.add_error('otp', 'Invalid OTP')
        return render(request, self.template_name, {'form': form})

from datetime import datetime

@method_decorator(login_required(login_url='login'), name='dispatch')    
class OrganizerHomeView(View):
    template_name = 'organizer/organizer_home.html'
    def get(self, request):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        organizer = Organizer.objects.filter(user = request.user).first()
        events_organized = Event.objects.filter(organizers = organizer)
        #Sort the events by date
        events_organized = sorted(events_organized, key = lambda x: x.start_date)
        current_date=datetime.now()

        print(current_date)
        return render(request, 'organizer/organizer_home.html', {'events': events_organized, 'current_date': current_date})

@method_decorator(login_required(login_url='login'), name='dispatch')   
class OrganizerEventView(View):
    def get(self, request, event_id):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        
        event = get_object_or_404(Event, pk=event_id)
        volunteers = Volunteer_event.objects.filter(event=event)
        volunteer_list = [x.volunteer for x in volunteers]
        venue_list = Venue_schedule_event.objects.filter(event=event)

        return render(request, 'organizer/organizer_event.html', {'event': event, 'volunteer_list': volunteer_list, 'venue_list': venue_list})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class OrganizerVolunteerView(View):
    def get(self, request):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        
        # get all volunteers and the events they are volunteering for
        volunteers = Volunteer.objects.all()
        volunteer_events = {}
        for volunteer in volunteers:
            volunteer_events[volunteer] = Volunteer_event.objects.filter(volunteer=volunteer)

        return render(request, 'organizer/organizer_volunteer.html', {'volunteer_events': volunteer_events})


@method_decorator(login_required(login_url='login'), name='dispatch')  
class OrganizerProfileView(View):
    def get(self, request):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        
        organizer = Organizer.objects.filter(user=request.user).first()
        return render(request, 'organizer/organizer_profile.html', {'organizer': organizer})
    

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_view(View):
    def get(self, request, *args, **kwargs):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("index")
        event_list = Event.objects.all()
        participant = External_Participant.objects.filter(user=request.user).first()
        registered = []
        for i in range (len(event_list)):
            registered.append(0)
        events_registered = Participant_event.objects.filter(participant=participant).values('event')
        registerd_event_ids = [x['event'] for x in events_registered]
        for i in range(len(event_list)):

            if(event_list[i].pk in registerd_event_ids):
                registered[i]=1
        print(registered,events_registered,event_list,"\n\n\n\n\n\n\n")
        return render(request,"participant/home.html",{'events':event_list,
                                                       'registered': registered
                                                       })
    
    def post(self,request,*args,**kwargs):
        return redirect('participant/')


@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_register_view(View):
    def get(self,request,event_id):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("index")
        event = get_object_or_404(Event, pk=event_id)
        participant = External_Participant.objects.filter(user=request.user).first()
        existing_participant_event = Participant_event.objects.filter(participant=participant, event=event).first()
        if existing_participant_event:
            return HttpResponse("You are already registered for this event.")
        new_participant_event = Participant_event(participant=participant, event=event)
        new_participant_event.save()
        return HttpResponse("You have successfully registered for the event.")
    def post(self, request, *args, **kwargs):
        return redirect('participant/')

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_event_view(View):
    def get(self, request, event_id):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("index")
        event_data = Event.objects.filter(pk=event_id).values('name','description','start_date','end_date','registration_end_date')
        event = Event.objects.filter(pk=event_id).first()
        print(event_data,"\n\n\n\n\n\n")
        participant = External_Participant.objects.filter(user=request.user).first()
        existing_participant_event = Participant_event.objects.filter(participant=participant, event=event).first()
        if not existing_participant_event:
            return HttpResponse("You are not registered for this event.")
        return render(request, 'participant/participant_event_view.html', context = event_data[0])

    def post(self, request, *args, **kwargs):
        return redirect('participant/')

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_profile_view(View):
    def get(self, request, *args, **kwargs):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("index")
        participant = External_Participant.objects.filter(user=request.user).first()
        return render(request, 'participant/participant_profile.html', {'participant': participant})
    def post(self, request, *args, **kwargs):
        return redirect('participant/')

@method_decorator(login_required(login_url='login'), name='dispatch')
class StudentHomeView(View):
    def get(self, request):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='student'):
            return redirect("index")
        events = list(Event.objects.all())

        #todo: filter live events

        return render(request, 'student/student_home.html', {'events': events})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class StudentProfileView(View):
    def get(self, request):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='student'):
            return redirect("index")
        student = Student.objects.filter(user=request.user).first()
        return render(request, 'student/student_profile.html', {'student': student})

#todo: check registration - seems like entity is not getting added

@method_decorator(login_required(login_url='login'), name='dispatch')
class StudentVolunteerView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return HttpResponse("You're not logged in")
        if request.user.role != 'student':
            return redirect("index")
        student = Student.objects.filter(user=request.user).first()
        volunteer = Volunteer.objects.filter(student=student).first()
        if volunteer is not None:
            # get events that the student has volunteered for
            volunteer_events = Volunteer_event.objects.filter(volunteer=volunteer)
            return render(request, 'student/student_volunteer.html', { 'events': volunteer_events})
        else:
            return render(request, 'student/student_register_volunteer.html', {'student': student})

@method_decorator(login_required(login_url='login'), name='dispatch')
class StudentRegisterVolunteerView(View):
    def post(self, request):
        student = Student.objects.filter(user=request.user).first()
        Volunteer.objects.create(student=student, hours=0)
        return redirect('student-volunteer')
        

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
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
def events(request):
    # Retrieve all events from the database
    events = Event.objects.all()
    return render(request, 'events/events.html', {'events': events})

