from django import forms
from .models import User_Entity, Student, Volunteer, External_Participant, Organizer

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
    telephoneNumber = forms.CharField(max_length=100, required=True)
    photograph = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices = [('', '---'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False, initial='')
    date_of_birth = forms.DateField(required=False)

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
    telephoneNumber = forms.CharField(max_length=100, required=True)
    photograph = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices = [('', '---'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False, initial='')
    date_of_birth = forms.DateField(required=False)

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