from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class User_Entity(AbstractUser, PermissionsMixin):
    first_name = models.CharField("first name", max_length=150, blank=False)
    middle_name = models.CharField("middle name", max_length=150, blank=True)
    last_name = models.CharField("last name", max_length=150, blank=False)
    email = models.EmailField("email address", blank=False)
    address_line_1 = models.CharField("Address Line 1", max_length=150, blank=False)
    address_line_2 = models.CharField("Address Line 2", max_length=150, blank=True,default="",null=False)
    state = models.CharField("City", max_length=150, blank=False)
    country = models.CharField("Country", max_length=150, blank=False)
    pin_code = models.CharField("PIN Code", max_length=150, blank=False)
    telephoneNumber = PhoneNumberField("Telephone Number", blank=False)
    photograph = models.ImageField("Photo", blank = True, null = True, upload_to = "images/")

    ROLES = [
        ('student', 'Student'),
        ('external_participant', 'External Participant'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin')
    ]
    
    role = models.CharField("Role", max_length=40, choices=ROLES, default='student', blank = False)

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField("Date of Birth", blank=True, null=True)

    is_active = models.BooleanField("Active", default=True, blank=False)

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
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    class Meta:
        verbose_name = "Organizer"
        verbose_name_plural = "Organizers"
        
class Organizer_Key(models.Model):
    key = models.CharField("Key", max_length = 100, primary_key = True, blank = False, unique = True)

    def __str__(self):
        return self.key
    
    class Meta:
        verbose_name = "Organizer Key"
        verbose_name_plural = "Organizer Keys"

class Venue(models.Model):
    name = models.CharField("venue_name",max_length=50,blank=False)
    capacity = models.IntegerField("venue_capacity",blank=False)
    address_line_1 = models.CharField("address_line_1",max_length=50,blank=False)
    address_line_2 = models.CharField("address_line_2",max_length=50,blank=True,default="",null=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    organizers = models.ManyToManyField(Organizer, related_name='events', blank=True)
    volunteers = models.ManyToManyField(Volunteer, related_name='events', blank=True)
    students = models.ManyToManyField(Student, related_name='events', blank=True)
    external_participants = models.ManyToManyField(External_Participant, related_name='events', blank=True)
    name = models.CharField("Event Name",max_length=50,blank=False)
    description = models.TextField("Event Description",blank=True)
    start_date = models.DateTimeField("Event Start Date",blank=False)
    end_date = models.DateTimeField("Event End Date",blank=False)
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE,null=True)
    registration_start_date = models.DateTimeField("Registration Start Date",blank=False)
    registration_end_date = models.DateTimeField("Registration End Date",blank=False)
    max_participants = models.IntegerField("Max Participants",blank=False)
    min_participants = models.IntegerField("Min Participants",blank=False)
    registered_participants = models.IntegerField("Registered Participants", default=0)

    def __str__(self):
        return self.name

class Accomodation(models.Model):
    accomodation_name = models.CharField(max_length=50,blank=False)
    address_line_1 = models.CharField(max_length=50,blank=False)
    address_line_2 = models.CharField(max_length=50,blank=True)
    cost_per_night = models.FloatField(blank=False)
    facilities = models.TextField(blank=True)
    contact = PhoneNumberField(blank=True)
    next_free_room = models.IntegerField(default = 101)

    def __str__(self):
        return self.accomodation_name

class Participant_Accomodation(models.Model):
    participant = models.ForeignKey(External_Participant,on_delete=models.CASCADE, related_name="participant_accomodation")
    accomodation = models.ForeignKey(Accomodation,on_delete=models.CASCADE, related_name="participant_accomodation")
    start_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)
    room_number = models.CharField(max_length=50,blank=False)

class EventResults(models.Model):
    event = models.OneToOneField(Event,on_delete=models.CASCADE, related_name="results", primary_key=True)
    result_description = models.TextField(blank=True)
    first_place = models.ForeignKey(User_Entity,on_delete=models.CASCADE,related_name="first_place",blank=True,null=True)
    second_place = models.ForeignKey(User_Entity,on_delete=models.CASCADE,related_name="second_place",blank=True,null=True)
    third_place = models.ForeignKey(User_Entity,on_delete=models.CASCADE,related_name="third_place",blank=True,null=True)

    def __str__(self):
        return f"Event Result: {self.result_description}"


