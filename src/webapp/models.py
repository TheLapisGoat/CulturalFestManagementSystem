from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin

class User_Entity(AbstractUser, PermissionsMixin):
    
    first_name = models.CharField("first name", max_length=150, blank=False)
    last_name = models.CharField("last name", max_length=150, blank=False)
    middle_name = models.CharField("middle name", max_length=150, blank=True)
    email = models.EmailField("email address", blank=False)
    
    ROLES = [
        ('volunteer', 'Volunteer'),
        ('student', 'Student'),
        ('external_participant', 'External Participant'),
        ('organizer', 'Organizer'),
    ]
    
    role = models.CharField("Role", max_length=40, choices=ROLES, default='student', blank = False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        
    address = models.TextField("Address", blank=False)
    telephoneNumber = PhoneNumberField("Telephone Number", blank=False)
    photograph = models.ImageField("Photo", blank = True)

    REQUIRED_FIELDS = ["email", "address", "telephoneNumber", "role", "first_name", "last_name"]