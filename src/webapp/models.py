from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User_Entity(AbstractUser, PermissionsMixin):
    
    first_name = models.CharField("first name", max_length=150, blank=False)
    middle_name = models.CharField("middle name", max_length=150, blank=True, null=True)
    last_name = models.CharField("last name", max_length=150, blank=False)
    email = models.EmailField("email address", blank=False)
    address_line_1 = models.CharField("Address Line 1", max_length=150, blank=False)
    address_line_2 = models.CharField("Address Line 2", max_length=150, blank=True, null=True)
    state = models.CharField("City", max_length=150, blank=False)
    country = models.CharField("Country", max_length=150, blank=False)
    pin_code = models.CharField("PIN Code", max_length=150, blank=False)
    telephoneNumber = PhoneNumberField("Telephone Number", blank=False)
    photograph = models.ImageField("Photo", blank = True, null = True, upload_to = 'profile_pictures/')

    
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

    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, blank=True, null=True)
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

    REQUIRED_FIELDS = ['roll_number', 'department']

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

    REQUIRED_FIELDS = ['organization']

class Organizer(models.Model):
    user = models.OneToOneField(User_Entity, on_delete = models.CASCADE, related_name = "organizer", primary_key = True, blank = False, unique = True)
    department = models.CharField("Department", max_length = 100, blank = False)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.department + ')'
    
    class Meta:
        verbose_name = "Organizer"
        verbose_name_plural = "Organizers"
    
    REQUIRED_FIELDS = ['department']
class Venue(models.Model):
    venue_id = models.IntegerField("venue_id",primary_key=True)
    venue_name = models.CharField("venue_name",max_length=50,blank=False)
    venue_capacity = models.IntegerField("venue_capacity",blank=False)
    address_line_1 = models.CharField("address_line_1",max_length=50,blank=False)
    address_line_2 = models.CharField("address_line_2",max_length=50,blank=True)


class Event(models.Model):
    event_id = models.IntegerField("event_id",primary_key=True)
    event_name = models.CharField("event_name",max_length=50,blank=False)
    event_description = models.TextField("event_description",blank=True)
    event_start_date = models.DateTimeField("event_start_date",blank=False)
    event_end_date = models.DateTimeField("event_end_date",blank=False)
    venue_id = models.ForeignKey(Venue,on_delete=models.CASCADE,null=True)
    registration_start = models.DateTimeField("registration_start",blank=False)
    registration_end = models.DateTimeField("registration_end",blank=False)
    max_participants = models.IntegerField("max_participants",blank=False)
    min_participants = models.IntegerField("min_participants",blank=False)

class Organized_by(models.Model):
    event_id = models.ForeignKey(Event,on_delete=models.CASCADE)
    organizer_id = models.ForeignKey(Organizer,on_delete=models.CASCADE)

class Infra_schedule(models.Model):
    schedule_id = models.IntegerField(primary_key=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
