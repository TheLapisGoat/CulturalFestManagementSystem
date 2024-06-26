import threading
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
from .forms import StudentRegistrationForm, OTPVerificationForm, External_ParticipantRegistrationForm, OrganizerRegistrationForm, VolunteerRegistrationForm, Event_Registration_Form,EventResultForm
from django.utils.decorators import method_decorator
import random

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
@method_decorator(login_required(login_url='login'), name='dispatch')  
class OrganizerAddResult(View):
    def get(self,request,event_id):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        # Student choices are in the form of: (roll number) first_name last_name
        students = Student.objects.all()
        student_choices = [('0','---')]
        student_choices += [(str(student.pk), '(' + str(student.roll_number) + ') ' + str(student.user.first_name) + ' ' + str(student.user.last_name)) for student in students]

        # External participant choices are in the form of: (organization) first_name last_name
        participants = External_Participant.objects.all()
        participant_choices = [('0','---')]
        participant_choices += [(str(participant.pk), '(' + str(participant.organization) + ') ' + str(participant.user.first_name) + ' ' + str(participant.user.last_name)) for participant in participants]
        request.session['register_current_role1'] = 'student'
        request.session['register_current_role2'] = 'student'
        request.session['register_current_role3'] = 'student'
        form = EventResultForm(options1=student_choices,options2=student_choices,options3=student_choices)
        return render(request, 'organizer/add_result.html', {'form': form,'default_role1':'student','default_role2':'student','default_role3':'student'})
    
    def post(self,request,event_id):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        students = Student.objects.all()
        student_choices = [('0','---')]
        student_choices += [(str(student.pk), '(' + str(student.roll_number) + ') ' + str(student.user.first_name) + ' ' + str(student.user.last_name)) for student in students]

        # External participant choices are in the form of: (organization) first_name last_name
        participants = External_Participant.objects.all()
        participant_choices = [('0','---')]
        participant_choices += [(str(participant.pk), '(' + str(participant.organization) + ') ' + str(participant.user.first_name) + ' ' + str(participant.user.last_name)) for participant in participants]

        action = request.POST.get('action')
        self.template_name = 'organization/add_result.html'
        if action == 'role_change1' or action == 'role_change2' or action == 'role_change3':
            
            role1 = request.session['register_current_role1']
            role2 = request.session['register_current_role2']
            role3 = request.session['register_current_role3']
            choice1 = choice2 = choice3 = None
            if action=='role_change1':
                role1 = request.POST.get('role1')
                request.session['register_current_role1'] = role1
            if action=='role_change2':
                role2 = request.POST.get('role2')
                request.session['register_current_role2'] = role2
            if action=='role_change3':
                role3 = request.POST.get('role3')
                request.session['register_current_role3'] = role3
            if role1 == 'student':
                choice1 = student_choices
            elif role1 == 'external_participant':
                choice1 = participant_choices
            if role2 == 'student':
                choice2 = student_choices
            elif role2 == 'external_participant':
                choice2 = participant_choices
            if role3 == 'student':
                choice3 = student_choices
            elif role3 == 'external_participant':
                choice3 = participant_choices
            
            #Checking for no 
            form = EventResultForm(options1=choice1,options2=choice2,options3=choice3)
            return render(request, 'organizer/add_result.html', {'form': form, 'default_role1': role1, 'default_role2': role2, 'default_role3': role3})
        form = None
        role1 = request.session['register_current_role1']
        role2 = request.session['register_current_role2']
        role3 = request.session['register_current_role3']
        choice1 = choice2 = choice3 = None
        if role1 == 'student':
            choice1 = student_choices
        elif role1 == 'external_participant':
            choice1 = participant_choices
        if role2 == 'student':
            choice2 = student_choices
        elif role2 == 'external_participant':
            choice2 = participant_choices
        if role3 == 'student':
            choice3 = student_choices
        elif role3 == 'external_participant':
            choice3 = participant_choices
        form = EventResultForm(choice1,choice2,choice3,request.POST)
        if(form.is_valid()):
            result1 = form.cleaned_data['result1']
            result2 = form.cleaned_data['result2']
            result3 = form.cleaned_data['result3']
            result_description = form.cleaned_data['result_description']

            event = Event.objects.get(pk=event_id)
            first_place = None
            second_place = None
            third_place = None
            if result1 != '0':
                if role1 == 'student':
                    first_place = Student.objects.get(pk=result1).user
                elif role1 == 'external_participant':
                    first_place = External_Participant.objects.get(pk=result1).user

            if result2 != '0':
                if role2 == 'student':
                    second_place = Student.objects.get(pk=result2).user
                elif role2 == 'external_participant':
                    second_place = External_Participant.objects.get(pk=result2).user

            if result3 != '0':
                if role3 == 'student':
                    third_place = Student.objects.get(pk=result3).user
                elif role3 == 'external_participant':
                    third_place = External_Participant.objects.get(pk=result3).user

            #If the result already exists, then update the result
            event_result = EventResults.objects.filter(event=event).first()
            if event_result:
                event_result.first_place = first_place
                event_result.second_place = second_place
                event_result.third_place = third_place
                event_result.result_description = result_description
                event_result.save()
                return redirect('organizer-home')

            event_result = EventResults.objects.create(event=event,first_place=first_place,second_place=second_place,third_place=third_place)
            if result_description:
                event_result.result_description = result_description
            event_result.save()
            return redirect('organizer-home')
        else:
            return render(request, 'organizer/add_result.html', {'form': form, 'default_role1': role1, 'default_role2': role2, 'default_role3': role3})
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
            user.save()
        
            #Creating the models corresponding to the role
            if role == 'student':
                student = Student.objects.create(
                    user = user,
                    roll_number = form.cleaned_data['roll_number'],
                    department = form.cleaned_data['department']
                )
                student.save()
            elif role == 'external_participant':
                participant = External_Participant.objects.create(
                    user = user,
                    organization = form.cleaned_data['organization']
                )
                participant.save()
                
            elif role == 'organizer':
                organizer = Organizer.objects.create(
                    user = user
                )
                organizer.save()

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
        
class Register_Event_View(View):
    template_name = "organizer/organizer_register_event.html"
    def get(self,request):
        form = Event_Registration_Form(user=request.user)
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = Event_Registration_Form(request.POST, user = request.user)
        if form.is_valid():
            # using organizers.set() to add multiple organizers
            organizers = form.cleaned_data['organizers']
            # add the current user as an organizer
            organizers |= Organizer.objects.filter(user=request.user)
            venue = form.cleaned_data['venue']
            venue = Venue.objects.get(pk = venue)

            #First checking for the availability of the venue
            events = Event.objects.filter(venue = venue)
            for event in events:
                if form.cleaned_data['start_date'] < event.end_date and form.cleaned_data['end_date'] > event.start_date:
                    messages.error(request, 'Venue not available for the given dates')
                    return render(request,self.template_name,{'form':form})
                
            #Checking if the registration occurs before the event and if the registration end date occurs before the event end date
            if form.cleaned_data['start_date'] < form.cleaned_data['registration_start_date_time']:
                messages.error(request, 'Registration start date should occur before the event start date')
                return render(request,self.template_name,{'form':form})
            if form.cleaned_data['end_date'] < form.cleaned_data['registration_end_date_time']:
                messages.error(request, 'Registration end date should occur before the event end date')
                return render(request,self.template_name,{'form':form})
            
            event = Event.objects.create(
                name = form.cleaned_data['event_name'],
                description = form.cleaned_data['event_description'],
                start_date = form.cleaned_data['start_date'],
                end_date = form.cleaned_data['end_date'],
                registration_start_date = form.cleaned_data['registration_start_date_time'],
                registration_end_date = form.cleaned_data['registration_end_date_time'],
                venue = venue,
                max_participants = form.cleaned_data['max_participants'],
                min_participants = form.cleaned_data['min_participants']
            )

            for organizer in organizers:
                event.organizers.add(organizer)
            event.save()

            return redirect('organizer-home')
        
        else:
            return render(request,self.template_name,{'form':form})

def schedule_deletion(request, extra_args):
    #Check if the user has verified the otp (is_active = True)
    user = User_Entity.objects.get(username = request.session['username'])
    if user.is_active == False:
        user.delete()
        
        #If the user is an organizer, then create the organizer key again
        if extra_args['role'] == 'organizer':
            organizer_key = Organizer_Key.objects.create(key = extra_args['organizer_key'])
            organizer_key.save()

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
                    return redirect('/login')
            else:
                return redirect('/register')
        else:
            return redirect('/login')
        
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
                        return render(request, 'registration/otp_verification.html', {'form': form, 'check': True})
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
        events_organized = organizer.events.all()
        print(events_organized,"\n\n\n\n\n")
        #Sort the events by date
        events_organized = sorted(events_organized, key = lambda x: x.start_date)
        current_date=datetime.now()

        print(current_date)
        return render(request, 'organizer/organizer_home.html', {'events': events_organized, 'current_date': current_date})
    
    def post(self, request):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        search_query = request.POST.get('search_query')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        #If the search query is empty, then return all events
        organizer = Organizer.objects.filter(user = request.user).first()
        events = organizer.events.all()
        if search_query:
            events = Event.objects.filter(name__icontains=search_query.lower())
        if start_date:
            events = events.filter(start_date__gte=start_date)
        if end_date:
            events = events.filter(end_date__lte=end_date)
        return render(request, 'organizer/organizer_home.html', {'events': events})

@method_decorator(login_required(login_url='login'), name='dispatch')   
class OrganizerEventView(View):
    def get(self, request, event_id):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        
        event = get_object_or_404(Event, pk=event_id)
        volunteer_list = event.volunteers.all()
        organizer_list = event.organizers.all()
        participant_count = event.students.count() + event.external_participants.count()
        venue = event.venue

        return render(request, 'organizer/organizer_event.html', {'event': event, 'volunteer_list': volunteer_list, 'venue': venue, 'organizer_list': organizer_list, 'participant_count': participant_count})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class OrganizerLogisticsView(View):
    def get(self, request):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        return render(request, 'organizer/organizer_logistics.html')


@method_decorator(login_required(login_url='login'), name='dispatch')  
class OrganizerProfileView(View):
    def get(self, request):
        if request.user.role != 'organizer':
            return redirect('index-redirector')
        
        organizer = Organizer.objects.filter(user=request.user).first()
        return render(request, 'organizer/organizer_profile.html', {'organizer': organizer})

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_home_api(View):
    def get(self, request):
        if request.user.role != 'external_participant':
            return redirect('index-redirector')
        
        participant = External_Participant.objects.get(user = request.user)
        registered_events = Event.objects.filter(external_participants = participant)
        unregistered_events = Event.objects.exclude(external_participants = participant)

        html_content = render(request, 'api/participant_home.html', {'unregistered_events': unregistered_events, 'registered_events': registered_events})
        return JsonResponse({'html_content': html_content.content.decode('utf-8')})
    
    def post(self, request):
        if request.user.role != 'external_participant':
            return redirect('index-redirector')
        
        search_query = request.POST.get('search_query')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        #If the search query is empty, then return all events
        participant = External_Participant.objects.get(user = request.user)
        events = Event.objects.all()
        if search_query:
            events = Event.objects.filter(name__icontains=search_query.lower())
        if start_date:
            events = events.filter(start_date__gte=start_date)
        if end_date:
            events = events.filter(end_date__lte=end_date)

        unregistered_events = Event.objects.exclude(external_participants = participant)
        # unregistered_events should only contain events contained in events
        unregistered_events = unregistered_events.filter(pk__in=events)

        registered_events = Event.objects.filter(external_participants = participant)

        html_content = render(request, 'api/participant_home.html', {'unregistered_events': unregistered_events, 'registered_events': registered_events})
        return JsonResponse({'html_content': html_content.content.decode('utf-8')})
        


@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_view(View):
    def get(self, request, *args, **kwargs):
        if request.user.role != 'external_participant':
            return redirect('index-redirector')
        
        participant = External_Participant.objects.get(user = request.user)
        registered_events = Event.objects.filter(external_participants = participant)
        unregistered_events = Event.objects.exclude(external_participants = participant)

        return render(request,"participant/participant_home.html",{'unregistered_events':unregistered_events,'registered_events':registered_events})


@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_register_view(View):
    def get(self,request,event_id):
        if request.user.role != 'external_participant':
            return redirect('index-redirector')
        event = get_object_or_404(Event, pk=event_id)
        participant = External_Participant.objects.filter(user=request.user).first()
        #if participant is already registered for the event
        if Event.objects.filter(external_participants = participant, pk=event_id).exists():
            return redirect('external-participant-home')
        
        #Adding the student as a participant for the event
        participant.events.add(event)
        participant.save()
        
        return render(request, 'participant/registration_success.html', {'event_name': event.name})

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_event_view(View):
    def get(self,request,event_id):
        if request.user.role != 'external_participant':
            return redirect('index-redirector')
        
        event_data = Event.objects.filter(pk=event_id).values('name','description','start_date','end_date','registration_end_date')
        # event = Event.objects.filter(pk=event_id).first()
        result = EventResults.objects.filter(event = event_id)

        return render(request, 'participant/participant_event_view.html',context = {'event':event_data[0],'result':result})

    def post(self, request, *args, **kwargs):
        return redirect('participant/')

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_profile_view(View):
    def get(self, request, *args, **kwargs):
        if request.user.role != 'external_participant':
            return redirect('index-redirector')
        participant = External_Participant.objects.filter(user=request.user).first()
        return render(request, 'participant/participant_profile.html', {'participant': participant})
    def post(self, request, *args, **kwargs):
        return redirect('participant/')
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_view_accomodation(View):
    def get(self,request, *args, **kwargs):
        if request.user.role != 'external_participant':
            return redirect('index-redirector')
        participant = External_Participant.objects.filter(user=request.user).first()
        accomodation_id = Participant_Accomodation.objects.get(participant=participant)
        accomodation = Accomodation.objects.get(pk=accomodation_id.accomodation.pk)
        return render(request, 'participant/participant_accomodation.html', {'accomodation': accomodation,'info':accomodation_id})

@method_decorator(login_required(login_url='login'), name='dispatch')
class student_home_api(View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        # Getting list of unregistered events (excluding both the events registered by the student as a participant and as a volunteer)
        events=Event.objects.all()
        unregistered_events = Event.objects.exclude(students=student)
        unregistered_events = unregistered_events.exclude(volunteers__student=student)
        
        # Getting list of events registered by the student as a participant
        events_registered_as_participant = student.events.all()
        
        # Getting list of events registered by the student as a volunteer
        events_registered_as_volunteer = Volunteer.objects.filter(student=student).values_list('events', flat=True)
        events_registered_as_volunteer = Event.objects.filter(pk__in=events_registered_as_volunteer)
        
        html_content = render(request, 'api/student_home.html', {'events':events,'unregistered_events': unregistered_events, 'events_registered_as_participant': events_registered_as_participant, 'events_registered_as_volunteer': events_registered_as_volunteer})
        return JsonResponse({'html_content': html_content.content.decode('utf-8')})
    
    def post(self, request):
        search_query = request.POST.get('search_query')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        #If the search query is empty, then return all events
        student = Student.objects.filter(user=request.user).first()
        events = Event.objects.all()
        if search_query:
            events = Event.objects.filter(name__icontains=search_query.lower())
        if start_date:
            events = events.filter(start_date__gte=start_date)
        if end_date:
            events = events.filter(end_date__lte=end_date)

        unregistered_events = Event.objects.exclude(students=student)
        unregistered_events = unregistered_events.exclude(volunteers__student=student)
        # unregistered_events should only contain events contained in events
        unregistered_events = unregistered_events.filter(pk__in=events)

        events_registered_as_participant = student.events.all()
        events_registered_as_participant = events_registered_as_participant.filter(pk__in=events)

        events_registered_as_volunteer = Volunteer.objects.filter(student=student).values_list('events', flat=True)
        events_registered_as_volunteer = Event.objects.filter(pk__in=events_registered_as_volunteer)
        events_registered_as_volunteer = events_registered_as_volunteer.filter(pk__in=events)

        html_content = render(request, 'api/student_home.html', {'unregistered_events': unregistered_events, 'events_registered_as_participant': events_registered_as_participant, 'events_registered_as_volunteer': events_registered_as_volunteer})
        return JsonResponse({'html_content': html_content.content.decode('utf-8')})

@method_decorator(login_required(login_url='login'), name='dispatch')
class student_home_view(View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('index-redirector')
        
        student = Student.objects.get(user=request.user)
        # Getting list of unregistered events (excluding both the events registered by the student as a participant and as a volunteer)
        unregistered_events = Event.objects.exclude(students=student)
        unregistered_events = unregistered_events.exclude(volunteers__student=student)
        
        # Getting list of events registered by the student as a participant
        events_registered_as_participant = student.events.all()
        
        # Getting list of events registered by the student as a volunteer
        events_registered_as_volunteer = Volunteer.objects.filter(student=student).values_list('events', flat=True)
        events_registered_as_volunteer = Event.objects.filter(pk__in=events_registered_as_volunteer)
        
        return render(request, 'student/student_home.html', {'unregistered_events': unregistered_events, 'events_registered_as_participant': events_registered_as_participant, 'events_registered_as_volunteer': events_registered_as_volunteer})


@method_decorator(login_required(login_url='login'), name='dispatch')
class student_register_event(View):
    def get(self,request,event_id):
        if request.user.role != 'student':
            return redirect('index-redirector')
        event = get_object_or_404(Event, pk=event_id)
        student = Student.objects.filter(user=request.user).first()
        #if student is already registered for the event
        if Event.objects.filter(students=student, pk=event_id).exists():
            return redirect('student-home')
        
        #Adding the student as a participant for the event
        student.events.add(event)
        student.save()
        
        return render(request, 'student/participant_registration_success.html', {'event_name': event.name})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class student_volunteer_for_event(View):
    def get(self, request, event_id):
        # Check if the user is a student
        if request.user.role != 'student':
            return redirect('index-redirector')
        
        # Get the event object
        event = get_object_or_404(Event, pk=event_id)
        
        # Get the student object
        student = Student.objects.filter(user=request.user).first()
        
        # Check if the student is already registered as a volunteer
        volunteer = Volunteer.objects.filter(student=student)
        if not volunteer:
            return redirect("student-register-volunteer")

        # Check if the student is already registered as a volunteer for the event
        if Event.objects.filter(volunteers__student=student, pk=event_id).exists():
            return redirect('student-volunteer-view-redirector')
        
        # Add the student as a volunteer for the event
        volunteer = volunteer[0]
        volunteer.events.add(event)
        volunteer.save()

        # Render the success page with redirect
        return render(request, 'student/registration_success.html', {'event_name': event.name})

@method_decorator(login_required(login_url='login'), name='dispatch')
class student_profile_view(View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('/logout/')
        student = Student.objects.filter(user=request.user).first()
        return render(request, 'student/student_profile.html', {'student': student})

@method_decorator(login_required(login_url='login'), name='dispatch')
class student_volunteer_redirect(View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('index-redirector')
        student = Student.objects.filter(user=request.user).first()
        volunteer = Volunteer.objects.filter(student=student).first()
        if volunteer is not None:
            return redirect('student-volunteer')
        else:
            return redirect('student-register-volunteer')

@method_decorator(login_required(login_url='login'), name='dispatch')
class student_register_volunteer_view(View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('index-redirector')
        form = VolunteerRegistrationForm()
        return render(request, 'student/student_register_volunteer.html', {'form': form})
    def post(self, request):
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            student = Student.objects.filter(user=request.user).first()
            volunteer = Volunteer.objects.create(student=student, hours=form.cleaned_data['hours'])
            volunteer.save()
            return redirect('student-volunteer')
        else:
            return render(request, 'student/student_register_volunteer.html', {'form': form})
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class student_volunteer_view(View):
    def get(self, request):
        if request.user.role != 'student':
            return redirect('index-redirector')
        #events is list of event that student is neither participant nor volunteer
        student = Student.objects.filter(user=request.user).first()
        events = Event.objects.exclude(students=student)
        events = events.exclude(volunteers__student=student)

        #volunteering_events is list of events that student is volunteer
        volunteering_events = Volunteer.objects.filter(student=student).values_list('events', flat=True)
        volunteering_events = Event.objects.filter(pk__in=volunteering_events)
        return render(request, 'student/student_volunteer.html', {'events': events,'volunteering_events':volunteering_events})
    
    def post(self, request):
        if request.user.role != 'student':
            return redirect('index-redirector')
        search_query = request.POST.get('search_query')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        #If the search query is empty, then return all events
        student = Student.objects.filter(user=request.user).first()
        filter_events = Event.objects.all()
        if search_query:
            filter_events = Event.objects.filter(name__icontains=search_query.lower())
        if start_date:
            filter_events = filter_events.filter(start_date__gte=start_date)
        if end_date:
            filter_events = filter_events.filter(end_date__lte=end_date)

        events = Event.objects.exclude(students=student)
        events = events.exclude(volunteers__student=student)
        events = events.filter(pk__in=filter_events)

        volunteering_events = Volunteer.objects.filter(student=student).values_list('events', flat=True)
        volunteering_events = Event.objects.filter(pk__in=volunteering_events)
        volunteering_events = volunteering_events.filter(pk__in=filter_events)
        return render(request, 'student/student_volunteer.html', {'events': events, 'volunteering_events': volunteering_events})
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class student_view_result(View):
    def get(self,request,event_id):
        if request.user.role != 'student':
            return redirect('index-redirector')
        
        event_data = Event.objects.filter(pk=event_id).values('name','description','start_date','end_date','registration_end_date')
        # event = Event.objects.filter(pk=event_id).first()
        result = EventResults.objects.filter(event = event_id)

        return render(request, 'student/student_event_view.html',context = {'event':event_data[0],'result':result})
    
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

