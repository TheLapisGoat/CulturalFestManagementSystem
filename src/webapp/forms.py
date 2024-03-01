from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User_Entity, Student, Volunteer, External_Participant, Organizer, Organizer_Key
from django.forms.widgets import *
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
    telephoneNumber = PhoneNumberField(
        max_length=100, required=True, widget=PhoneNumberPrefixWidget(region='IN'))
    photograph = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices = [('', '---'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False, initial='')
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1900, 2024))
                                    , required=False)

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
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1900, 2024))
                                    , required=False)

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
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1900, 2024))
                                    , required=False)

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
    event_name = forms.CharField(max_length=100, required=True)
    event_description = forms.CharField(max_length=100, required=True)
    start_date = forms.DateField(widget=SelectDateWidget, required=True)