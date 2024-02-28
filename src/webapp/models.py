from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User_Entity(AbstractUser, PermissionsMixin):
    
    first_name = models.CharField("first name", max_length=150, blank=False)
    middle_name = models.CharField("middle name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=False)
    email = models.EmailField("email address", blank=False)
    address_line_1 = models.CharField("Address Line 1", max_length=150, blank=False)
    address_line_2 = models.CharField("Address Line 2", max_length=150, blank=True)
    state = models.CharField("City", max_length=150, blank=False)
    country = models.CharField("Country", max_length=150, blank=False)
    pin_code = models.CharField("PIN Code", max_length=150, blank=False)
    telephoneNumber = PhoneNumberField("Telephone Number", blank=False)
    photograph = models.ImageField("Photo", blank = True)

    
    ROLES = [
        ('student', 'Student'),
        ('external_participant', 'External Participant'),
        ('organizer', 'Organizer'),
    ]
    
    role = models.CharField("Role", max_length=40, choices=ROLES, default='student', blank = False)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField("Date of Birth", blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'address_line_1', 'state', 'country', 'pin_code', 'telephoneNumber', 'role']

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    
class Student(models.Model):
    user = models.OneToOneField(User_Entity, on_delete = models.CASCADE, related_name = "student", primary_key = True, blank = False, unique = True)
    roll_number = models.CharField("Roll Number", max_length = 100, blank = False, unique = True)
    department = models.CharField("Department", max_length = 100, blank = False)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.roll_number + ')'
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Volunteer(models.Model):
    student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "volunteer", primary_key = True, blank = False, unique = True)
    hours = models.IntegerField("Hours", blank = False)

    def __str__(self):
        return self.student.user.first_name + ' ' + self.student.user.last_name + ' (' + self.student.roll_number + ')'
    
    class Meta:
        verbose_name = "Volunteer"
        verbose_name_plural = "Volunteers"

class External_Participant(models.Model):
    user = models.OneToOneField(User_Entity, on_delete = models.CASCADE, related_name = "external_participant", primary_key = True, blank = False, unique = True)
    organization = models.CharField("Organization", max_length = 100, blank = False)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.organization + ')'
    
    class Meta:
        verbose_name = "External Participant"
        verbose_name_plural = "External Participants"

class Organizer(models.Model):
    user = models.OneToOneField(User_Entity, on_delete = models.CASCADE, related_name = "organizer", primary_key = True, blank = False, unique = True)
    department = models.CharField("Department", max_length = 100, blank = False)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.department + ')'
    
    class Meta:
        verbose_name = "Organizer"
        verbose_name_plural = "Organizers"