from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User_Entity, Student, Volunteer, External_Participant, Organizer, Organizer_Key, Venue
from django.forms.widgets import *
from django.db.models import Q
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
#Whoever is reading this, THESE FORMS ARE MEANT FOR USE BY THE ADMIN SITE, DO NOT USE THEM ANYWHERE ELSE
class User_EntityCreationForm(UserCreationForm):
    class Meta:
        model = User_Entity
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'address_line_1', 'address_line_2', 'state', 'country', 'pin_code', 'telephoneNumber', 'photograph', 'gender', 'date_of_birth', 'is_active')

class User_EntityChangeForm(UserChangeForm):
    class Meta:
        model = User_Entity
        fields = ('username', 'first_name', 'last_name', 'email', 'role', 'address_line_1', 'address_line_2', 'state', 'country', 'pin_code', 'telephoneNumber', 'photograph', 'gender', 'date_of_birth', 'is_active')

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_number', 'department')

class StudentChangeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('roll_number', 'department')

class VolunteerCreationForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('student', 'hours')

class VolunteerChangeForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('student', 'hours')

class External_ParticipantCreationForm(forms.ModelForm):
    class Meta:
        model = External_Participant
        fields = ('organization',)

class External_ParticipantChangeForm(forms.ModelForm):
    class Meta:
        model = External_Participant
        fields = ('organization',)

class OrganizerCreationForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ()

class OrganizerChangeForm(forms.ModelForm):
    class Meta:
        model = Organizer
        fields = ()



class StudentRegistrationForm(forms.Form):

    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    roll_number = forms.CharField(max_length=100, required=True)
    department = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    middle_name = forms.CharField(max_length=150, required=False)
    address_line_1 = forms.CharField(max_length=100, required=True)
    address_line_2 = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=True)
    country = forms.CharField(max_length=100, required=True)
    pin_code = forms.CharField(max_length=100, required=True)
    telephoneNumber = PhoneNumberField(max_length=100, required=True, widget=PhoneNumberPrefixWidget(region='IN'))
    photograph = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices = [('', '---'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False, initial='')
    date_of_birth = forms.DateField(
        label="Date of Birth",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match")
            return False
        username = self.cleaned_data.get('username')
        user = User_Entity.objects.filter(username = username)
        if user.exists():
            self.add_error('username', "Username already exists")
            return False
        email = self.cleaned_data.get('email')
        user = User_Entity.objects.filter(email = email)
        if user.exists():
            self.add_error('email', "Email already exists")
            return False
        roll_number = self.cleaned_data.get('roll_number')
        student = Student.objects.filter(roll_number = roll_number)
        if student.exists():
            self.add_error('roll_number', "Roll Number already exists")
            return False

        return True
    
class OTPVerificationForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off'}))

class External_ParticipantRegistrationForm(forms.Form):

    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    organization = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    middle_name = forms.CharField(max_length=150, required=False)
    address_line_1 = forms.CharField(max_length=100, required=True)
    address_line_2 = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=True)
    country = forms.CharField(max_length=100, required=True)
    pin_code = forms.CharField(max_length=100, required=True)
    telephoneNumber = PhoneNumberField(
        max_length=100, required=True, widget=PhoneNumberPrefixWidget(region='IN'))
    photograph = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices = [('', '---'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False, initial='')
    date_of_birth = forms.DateField(
        label="Date of Birth",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match")
            return False
        username = self.cleaned_data.get('username')
        user = User_Entity.objects.filter(username = username)
        if user.exists():
            self.add_error('username', "Username already exists")
            return False
        email = self.cleaned_data.get('email')
        user = User_Entity.objects.filter(email = email)
        if user.exists():
            self.add_error('email', "Email already exists")
            return False

        return True
    
class OrganizerRegistrationForm(forms.Form):

    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    organizer_key = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    middle_name = forms.CharField(max_length=150, required=False)
    address_line_1 = forms.CharField(max_length=100, required=True)
    address_line_2 = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=True)
    country = forms.CharField(max_length=100, required=True)
    pin_code = forms.CharField(max_length=100, required=True)
    telephoneNumber = PhoneNumberField(
        max_length=100, required=True, widget=PhoneNumberPrefixWidget(region='IN'))
    photograph = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices = [('', '---'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False, initial='')
    date_of_birth = forms.DateField(
        label="Date of Birth",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match")
            return False
        username = self.cleaned_data.get('username')
        user = User_Entity.objects.filter(username = username)
        if user.exists():
            self.add_error('username', "Username already exists")
            return False
        email = self.cleaned_data.get('email')
        user = User_Entity.objects.filter(email = email)
        if user.exists():
            self.add_error('email', "Email already exists")
            return False
        
        organizer_key = self.cleaned_data.get('organizer_key')
        #Check if the organizer key is valid
        key = Organizer_Key.objects.filter(key = organizer_key)
        if not key.exists():
            self.add_error('organizer_key', "Invalid Organizer Key")
            return False

        return True
    
class VolunteerRegistrationForm(forms.Form):

    hours = forms.IntegerField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            return valid
        hours = self.cleaned_data.get('hours')
        if hours < 0:
            self.add_error('hours', "Hours cannot be negative")
            return False

        return True
    
class Event_Registration_Form(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        else: self.user = None
        super(Event_Registration_Form, self).__init__(*args, **kwargs)
        self.queryset = Organizer.objects.filter(~Q(user = self.user))
        self. fields['event_name'] = forms.CharField(max_length=100, required=True)
        self.fields['event_description'] = forms.CharField(max_length=100, required=True)
        venue_list = Venue.objects.all()
        venue_choices = [(venue.pk, venue.name) for venue in venue_list]
        self.fields['venue'] = forms.ChoiceField(choices = venue_choices, required=True)
        self.fields['start_date'] = forms.DateTimeField(
            label="Start Date Time", 
            required=True,
            widget=forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"}),
            input_formats=["%Y-%m-%d %H:%M"]
        )
        self.fields['end_date'] = forms.DateTimeField(
            label="End Date Time",
            required=True,
            widget=forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"}),
            input_formats=["%Y-%m-%d %H:%M"]
        )
        self.fields['registration_start_date_time'] = forms.DateTimeField(
            label="Registration Start Date Time",
            required=True,
            widget=forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"}),
            input_formats=["%Y-%m-%d %H:%M"]
        )
        self.fields['registration_end_date_time'] = forms.DateTimeField(
            label="Registration End Date Time",
            required=True,
            widget=forms.DateTimeInput(format="%Y-%m-%d %H:%M", attrs={"type": "datetime-local"}),
            input_formats=["%Y-%m-%d %H:%M"]
        )
        self.fields['max_participants'] = forms.IntegerField(required=True)
        self.fields['min_participants'] = forms.IntegerField(required=True)
        self.fields['organizers'] = forms.ModelMultipleChoiceField(queryset=self.queryset, required=False, widget=forms.CheckboxSelectMultiple)

    def clean(self) -> dict[str, Any]:
        return super().clean()
    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            print("SUPER NOT VALID")
            return valid
        print("\n\n CHECKING OTHER THIGNS\n")
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        registration_start_date_time = self.cleaned_data.get('registration_start_date_time')
        registration_end_date_time = self.cleaned_data.get('registration_end_date_time')
        if start_date > end_date:
            self.add_error('end_date', "End Date cannot be before Start Date")
            print("End Date cannot be before Start Date")
            return False
        if registration_start_date_time > registration_end_date_time:
            self.add_error('registration_end_date_time', "Registration End Date Time cannot be before Registration Start Date Time")
            print("Registration End Date Time cannot be before Registration Start Date Time")
            return False
        max_participants = self.cleaned_data.get('max_participants')
        min_participants = self.cleaned_data.get('min_participants')
        if max_participants < 0:
            self.add_error('max_participants', "Max Participants cannot be negative")
            print("Max Participants cannot be negative")
            return False
        if min_participants < 0:
            self.add_error('min_participants', "Min Participants cannot be negative")
            print("Min Participants cannot be negative")
            return False
        if max_participants < min_participants:
            self.add_error('max_participants', "Max Participants cannot be less than Min Participants")
            print("Max Participants cannot be less than Min Participants")
            return False
        return True
    


class EventResultForm(forms.Form):
    def __init__(self, options1,options2,options3, *args, **kwargs):
        super(EventResultForm, self).__init__(*args, **kwargs)
        self.options1 = options1
        self.options2 = options2
        self.options3 = options3
        self.fields['result1'] = forms.ChoiceField(choices = self.options1, required=False)
        self.fields['result2'] = forms.ChoiceField(choices = self.options2, required=False)
        self.fields['result3'] = forms.ChoiceField(choices = self.options3, required=False)
        self.fields['result_description'] = forms.CharField(widget=forms.Textarea, label='Multi-line Text Field', required=False)




