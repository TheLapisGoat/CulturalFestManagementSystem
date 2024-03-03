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
from .forms import StudentRegistrationForm, OTPVerificationForm, External_ParticipantRegistrationForm, OrganizerRegistrationForm, VolunteerRegistrationForm, Event_Registration_Form,EventResultForm
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
@method_decorator(login_required(login_url='login'), name='dispatch')  
class OrganizerAddResult(View):
    def get(self,request,event_id):
        if request.user.role != 'organizer':
            return redirect('/logout/')
        students = Student.objects.all()
        student_primary_keys = Student.objects.all().values('pk')
        student_names = [str(k) for k in students]
        participants = External_Participant.objects.all()
        participant_primary_keys = External_Participant.objects.all().values('pk')
        participant_names = [str(k) for k in participants]
        student_choices = [(str(pk), name) for pk, name in zip(student_primary_keys, student_names)]
        participant_choices = [(str(pk), name) for pk, name in zip(participant_primary_keys, participant_names)]
        request.session['register_current_role1'] = 'student'
        request.session['register_current_role2'] = 'student'
        request.session['register_current_role3'] = 'student'
        form = EventResultForm(options1=student_choices,options2=student_choices,options3=student_choices)
        return render(request, 'organizer/add_result.html', {'form': form,'default_role1':'student','default_role2':'student','default_role3':'student'})
    
    def post(self,request,event_id):
        if request.user.role != 'organizer':
            return redirect('/logout/')
        students = Student.objects.all()
        student_primary_keys = Student.objects.all().values('pk')
        student_names = [str(k) for k in students]
        participants = External_Participant.objects.all()
        participant_primary_keys = External_Participant.objects.all().values('pk')
        participant_names = [str(k) for k in participants]
        student_choices = [(str(pk), name) for pk, name in zip(student_primary_keys, student_names)]
        participant_choices = [(str(pk), name) for pk, name in zip(participant_primary_keys, participant_names)]
        action = request.POST.get('action')
        self.template_name = 'organization/add_result.html'
        if action == 'role_change1' or action == 'role_change2' or action == 'role_change3':
            
            form = None
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
            result1 = int(form.cleaned_data['result1'][6:-1])
            result2 = int(form.cleaned_data['result2'][6:-1])
            result3 = int(form.cleaned_data['result3'][6:-1])
            print(result1,result2,result3,'\n\n\n\n\n')
            event = Event.objects.get(pk=event_id)
            role1 = request.session['register_current_role1']
            role2 = request.session['register_current_role2']
            role3 = request.session['register_current_role3']
            existing_results = EventResults.objects.filter(event=event)
            if existing_results:
                existing_results.delete()
            choice1 = choice2 = choice3 = None
            if role1 == 'student':
                choice1 = ContentType.objects.get_for_model(Student)
            elif role1 == 'external_participant':
                choice1 = ContentType.objects.get_for_model(External_Participant)
            if role2 == 'student':
                choice2 = ContentType.objects.get_for_model(Student)
            elif role2 == 'external_participant':
                choice2 = ContentType.objects.get_for_model(External_Participant)
            if role3 == 'student':
                choice3 = ContentType.objects.get_for_model(Student)
            elif role3 == 'external_participant':
                choice3 = ContentType.objects.get_for_model(External_Participant)
            eventresults = EventResults.objects.create(event=event,
                                                       first_place_content_type=choice1,
                                                       first_place_object_id=result1,
                                                       second_place_content_type=choice2,
                                                       second_place_object_id=result2,
                                                       third_place_content_type=choice3,
                                                       third_place_object_id=result3,
                                                       result_description=form.cleaned_data['result_description']
                                )
            eventresults.save()
            messages.success(request, 'Results added successfully')
            return redirect('organizer-home')
       
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
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='organizer'):
            return redirect("/logout/")
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = Event_Registration_Form(request.POST, user = request.user)
        if form.is_valid():
            # using organizers.set() to add multiple organizers
            organizers = form.cleaned_data['organizers']
            print(organizers)
            # add the current user as an organizer
            organizers |= Organizer.objects.filter(user=request.user)
            venue = form.cleaned_data['venue']
            venue = Venue.objects.get(pk = venue)
            print(organizers)
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
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            infra_schedule = Infra_schedule.objects.create(start_time = start_date, end_time = end_date)
            infra_schedule.save()
            venue_schedule_event = Venue_schedule_event.objects.create(event = event, venue = venue, schedule = infra_schedule)
            venue_schedule_event.save()
            return redirect('organizer-home')
        else:
            # for field in form:
            #     print(field, field.errors)
            # print(form.errors)
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
            return redirect('/logout/')
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
            return redirect('/logout/')
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
            return redirect('/logout/')
        
        event = get_object_or_404(Event, pk=event_id)
        volunteers = Volunteer_event.objects.filter(event=event)
        volunteer_list = [x.volunteer for x in volunteers]
        venue_list = Venue_schedule_event.objects.filter(event=event)

        return render(request, 'organizer/organizer_event.html', {'event': event, 'volunteer_list': volunteer_list, 'venue_list': venue_list})
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class OrganizerLogisticsView(View):
    def get(self, request):
        if request.user.role != 'organizer':
            return redirect('/logout/')
        return render(request, 'organizer/organizer_logistics.html')


@method_decorator(login_required(login_url='login'), name='dispatch')  
class OrganizerProfileView(View):
    def get(self, request):
        if request.user.role != 'organizer':
            return redirect('/logout/')
        
        organizer = Organizer.objects.filter(user=request.user).first()
        return render(request, 'organizer/organizer_profile.html', {'organizer': organizer})
    


@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_view(View):
    def get(self, request, *args, **kwargs):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("/logout/")
        
        events = list(Event.objects.all())
        participant = External_Participant.objects.get(user = request.user)
        participant_events = Participant_event.objects.filter(participant = participant).values('event')
        participant_events = [x['event'] for x in participant_events]
        events_registered = [x for x in events if x.pk in participant_events]
        events = [x for x in events if x.pk not in participant_events]
        return render(request,"participant/home.html",{'events':events,'events_registered':events_registered})
    
    def post(self, request):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("/logout/")
        search_query = request.POST.get('search_query')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        #If the search query is empty, then return all events
        participant = External_Participant.objects.filter(user=request.user).first()
        events = Event.objects.all()
        if search_query:
            events = Event.objects.filter(name__icontains=search_query.lower())
        if start_date:
            events = events.filter(start_date__gte=start_date)
        if end_date:
            events = events.filter(end_date__lte=end_date)
        return render(request, 'student/student_home.html', {'events': events})


@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_register_view(View):
    def get(self,request,event_id):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("/logout/")
        event = get_object_or_404(Event, pk=event_id)
        participant = External_Participant.objects.filter(user=request.user).first()
        existing_participant_event = Participant_event.objects.filter(participant=participant, event=event).first()
        if existing_participant_event:
            return HttpResponse("You are already registered for this event.")
        new_participant_event = Participant_event(participant=participant, event=event)
        new_participant_event.save()
        event.registered_participants += 1
        event.save()
        return HttpResponse("You have successfully registered for the event.")
    def post(self, request, *args, **kwargs):
        return redirect('participant/')

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_event_view(View):
    def get(self, request, event_id):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("/logout/")
        event_data = Event.objects.filter(pk=event_id).values('name','description','start_date','end_date','registration_end_date')
        event = Event.objects.filter(pk=event_id).first()
        print(event_data,"\n\n\n\n\n\n")
        participant = External_Participant.objects.filter(user=request.user).first()
        result = EventResults.objects.filter(event=event_id)
        if(result):
            result = result[0]
            if(result.get_first_place_type()==Student):
                first = Student.objects.filter(pk=result.first_place_object_id)
                print(result.first_place_object_id, first,"\n\n\n\n")
                participants = External_Participant.objects.all()
                for participant in participants:
                    print(participant.pk)
                first_place = str(first[0])
            elif(result.get_first_place_type()==External_Participant):
                first = External_Participant.objects.filter(pk=result.first_place_object_id)
                first_place = str(first[0])
            if(result.get_second_place_type()==Student):
                second = Student.objects.filter(pk=result.second_place_object_id)
                second_place = str(second[0])
            elif(result.get_second_place_type()==External_Participant):
                second = External_Participant.objects.filter(pk=result.second_place_object_id)
                second_place = str(second[0])
            if(result.get_third_place_type()==Student):
                third = Student.objects.filter(pk=result.third_place_object_id)
                third_place = str(third[0])
            elif(result.get_third_place_type()==External_Participant):
                third = External_Participant.objects.filter(pk=result.third_place_object_id)
                third_place = str(third[0])
        else:
            first_place=None
            second_place=None
            third_place=None
        context1 = {'first_place':first_place,'second_place':second_place,'third_place':third_place}
        merged_context = {**event_data[0], **context1}
        existing_participant_event = Participant_event.objects.filter(participant=participant, event=event).first()
        if not existing_participant_event:
            return HttpResponse("You are not registered for this event.")
        return render(request, 'participant/participant_event_view.html',context = merged_context)

    def post(self, request, *args, **kwargs):
        return redirect('participant/')

@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_profile_view(View):
    def get(self, request, *args, **kwargs):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("/logout/")
        participant = External_Participant.objects.filter(user=request.user).first()
        return render(request, 'participant/participant_profile.html', {'participant': participant})
    def post(self, request, *args, **kwargs):
        return redirect('participant/')
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class participant_view_accomodation(View):
    def get(self,request, *args, **kwargs):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='external_participant'):
            return redirect("/logout/")
        participant = External_Participant.objects.filter(user=request.user).first()
        accomodation_id = Participant_Accomodation.objects.get(participant=participant)
        accomodation = Accomodation.objects.get(pk=accomodation_id.accomodation.pk)
        return render(request, 'participant/participant_accomodation.html', {'accomodation': accomodation,'info':accomodation_id})

@method_decorator(login_required(login_url='login'), name='dispatch')
class student_home_view(View):
    def get(self, request):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='student'):
            return redirect("/logout/")
        student = Student.objects.get(user=request.user)
        participant_events = StudentEvent.objects.filter(student = student).values('event')
        participant_events = [x['event'] for x in participant_events]
        events = list(Event.objects.all())
        events_registered = [x for x in events if x.pk in participant_events]
        volunteer = Volunteer.objects.filter(student = student)
        events_volunteered = []
        if(volunteer):
            volunteer = volunteer[0]
            volunteer_events = Volunteer_event.objects.filter(volunteer = volunteer).values('event')
            volunteer_events = [x['event'] for x in volunteer_events]
            events_volunteered = [x for x in events if x.pk in volunteer_events]
        print("Hello",volunteer_events,events_volunteered,"\n\n\n\n")
        events_registered = [x for x in events if x.pk in participant_events or x.pk in volunteer_events]
        events = [x for x in events if x.pk not in participant_events and x.pk not in volunteer_events]
        print(events,events_registered,"\n\n\n\n")
        return render(request, 'student/student_home.html', {'events': events,'events_registered': events_registered})
    
    def post(self, request):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='student'):
            return redirect("/logout/")
        search_query = request.POST.get('search_query')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        #If the search query is empty, then return all events
        events = Event.objects.all()
        if search_query:
            events = Event.objects.filter(name__icontains=search_query.lower())
        if start_date:
            events = events.filter(start_date__gte=start_date)
        if end_date:
            events = events.filter(end_date__lte=end_date)
        return render(request, 'student/student_home.html', {'events': events})

@method_decorator(login_required(login_url='login'), name='dispatch')
class student_register_event(View):
    def get(self,request,event_id):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='student'):
            return redirect("/logout/")
        event = get_object_or_404(Event, pk=event_id)
        student = Student.objects.filter(user=request.user).first()
        existing_participant_event = StudentEvent.objects.filter(student=student, event=event).first()
        if existing_participant_event:
            return HttpResponse("You are already registered for this event.")
        new_participant_event = StudentEvent(student=student, event=event)
        new_participant_event.save()
        event.registered_participants += 1
        event.save()
        return HttpResponse("You have successfully registered for the event.")
    def post(self, request, *args, **kwargs):
        return redirect('student/')
    
import random
@method_decorator(login_required(login_url='login'), name='dispatch')
class student_volunteer(View):
    def get(self,request,event_id):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='student'):
            return redirect("/logout/")
        event = get_object_or_404(Event, pk=event_id)
        student = Student.objects.filter(user=request.user).first()
        volunteer = Volunteer.objects.filter(student=student)
        if(not volunteer):
            return redirect("/student/register_volunteer/")
        existing_volunteer_event = Volunteer_event.objects.filter(volunteer=volunteer[0], event=event).first()
        if existing_volunteer_event:
            return HttpResponse("You are already registered as a volunteer for this event.")
        new_volunteer_event = Volunteer_event(volunteer=volunteer[0], event=event)
        new_volunteer_event.save()
        return HttpResponse("You have successfully registered as a volunteer for the event.")
    
    def post(self, request, *args, **kwargs):
        return redirect('student/')
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
        if request.user.is_anonymous:
            return HttpResponse("You're not logged in")
        if request.user.role != 'student':
            return redirect("/logout/")
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
            return redirect('/logout/')
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
            return redirect('/logout/')
        student = Student.objects.filter(user=request.user).first()
        volunteer = Volunteer.objects.filter(student=student).first()
        events = list(Event.objects.all())
        volunteer_events = Volunteer_event.objects.filter(volunteer=volunteer).values('event')
        volunteer_events = [x['event'] for x in volunteer_events]
        volunteering_events = [x for x in events if x.pk in volunteer_events]
        student_events = StudentEvent.objects.filter(student=student).values('event')
        student_events = [x['event'] for x in student_events]
        events = [x for x in events if x.pk not in student_events]
        events = [x for x in events if x.pk not in volunteer_events]
        print(events,'\n\n\n\n\n')
        return render(request, 'student/student_volunteer.html', {'events': events,'volunteering_events':volunteering_events})
        
@method_decorator(login_required(login_url='login'), name='dispatch')
class student_view_result(View):
    def get(self,request,event_id):
        if(request.user.is_anonymous):
            return HttpResponse("You're not logged in")
        if(request.user.role!='student'):
            return redirect("/logout/")
        event_data = Event.objects.filter(pk=event_id).values('name','description','start_date','end_date','registration_end_date')
        event = Event.objects.filter(pk=event_id).first()
        print(event_data,"\n\n\n\n\n\n")
        participant = Student.objects.filter(user=request.user).first()
        result = EventResults.objects.filter(event=event_id)
        if(result):
            result = result[0]
            if(result.get_first_place_type()==Student):
                first = Student.objects.filter(pk=result.first_place_object_id)
                print(result.first_place_object_id, first,"\n\n\n\n")
                participants = External_Participant.objects.all()
                for participant in participants:
                    print(participant.pk)
                first_place = str(first[0])
            elif(result.get_first_place_type()==External_Participant):
                first = External_Participant.objects.filter(pk=result.first_place_object_id)
                first_place = str(first[0])
            if(result.get_second_place_type()==Student):
                second = Student.objects.filter(pk=result.second_place_object_id)
                second_place = str(second[0])
            elif(result.get_second_place_type()==External_Participant):
                second = External_Participant.objects.filter(pk=result.second_place_object_id)
                second_place = str(second[0])
            if(result.get_third_place_type()==Student):
                third = Student.objects.filter(pk=result.third_place_object_id)
                third_place = str(third[0])
            elif(result.get_third_place_type()==External_Participant):
                third = External_Participant.objects.filter(pk=result.third_place_object_id)
                third_place = str(third[0])
        else:
            first_place=None
            second_place=None
            third_place=None
        context1 = {'first_place':first_place,'second_place':second_place,'third_place':third_place}
        merged_context = {**event_data[0], **context1}
        student = Student.objects.get(user = request.user)
        existing_participant_event = StudentEvent.objects.filter(student=student, event=event).first()
        volunteer = Volunteer.objects.filter(student = student)
        existing_volunteer_event = None
        if(volunteer):
            volunteer = volunteer[0]
            existing_volunteer_event = Volunteer_event.objects.filter(volunteer=volunteer, event=event).first()
        if (not existing_participant_event) and (not existing_volunteer_event):
            return HttpResponse("You are not registered for this event.")
        return render(request, 'student/student_event_view.html',context = merged_context)
    def post(self, request, *args, **kwargs):
        return redirect('student/')
        
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

